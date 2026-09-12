const fs = require('fs');
const path = require('path');
const { chromium, firefox, webkit } = require('playwright');

const browserTypes = { chromium, firefox, webkit };
const base = process.env.AINOS_TEST_BASE || 'http://127.0.0.1:4173';
const outputDir = process.env.AINOS_QA_OUTPUT || 'cross-browser-results';
const screenshotDir = path.join(outputDir, 'screenshots');
const rows = [];
const failures = [];
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

fs.mkdirSync(screenshotDir, { recursive: true });

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

async function pageState(page) {
  return page.evaluate(() => {
    const hero = document.querySelector('.hero-shell');
    const brand = document.querySelector('.brand-mark-img');
    const h1 = document.querySelector('h1');
    const root = document.documentElement;
    return {
      overflow: root.scrollWidth - root.clientWidth,
      heroWidth: hero?.getBoundingClientRect().width || 0,
      heroHeight: hero?.getBoundingClientRect().height || 0,
      h1Size: h1 ? parseFloat(getComputedStyle(h1).fontSize) : 0,
      focusCount: document.querySelectorAll('#focus .focus-card').length,
      teamCount: document.querySelectorAll('#team .person').length,
      brandLoaded: Boolean(brand && brand.complete && brand.naturalWidth > 0),
      currentYear: document.querySelector('[data-current-year]')?.textContent?.trim() || ''
    };
  });
}

async function validateFounderImages(page, language) {
  await page.locator('#team').scrollIntoViewIfNeeded();
  await page.waitForFunction(() => {
    const founders = [...document.querySelectorAll('#team .person-photo')];
    return founders.length === 2 && founders.every(img => img.complete && img.naturalWidth > 0 && img.naturalHeight > 0);
  }, null, { timeout: 5000 });

  const valid = await page.evaluate(() => {
    const founders = [...document.querySelectorAll('#team .person-photo')];
    return founders.length === 2 && founders.every(img => img.complete && img.naturalWidth > 0 && img.naturalHeight > 0);
  });
  assert(valid, `${language}: lazy founder imagery failed after Team entered the viewport`);
}

async function validateSkipLink(page, language) {
  await page.keyboard.press('Tab');
  const focusedHref = await page.evaluate(() => document.activeElement?.getAttribute('href') || '');
  assert(focusedHref === '#main-content', `${language}: first keyboard stop must be skip-to-content`);

  // The link animates into view over 160 ms. Wait for its settled focused state
  // instead of sampling its transformed off-screen position on the same frame.
  await page.waitForFunction(() => {
    const active = document.activeElement;
    if (!active || !active.classList.contains('skip-link')) return false;
    const rect = active.getBoundingClientRect();
    return rect.width > 0 && rect.height > 0 && rect.top >= 0 && rect.bottom > 0 && rect.right > 0;
  }, null, { timeout: 1200 });
}

async function validateDesktop(browserName, browser, language) {
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    reducedMotion: 'no-preference'
  });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', err => errors.push(String(err)));
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });

  try {
    const response = await page.goto(`${base}/${language}/`, { waitUntil: 'networkidle' });
    assert(response && response.status() === 200, `${language}: expected HTTP 200`);
    assert(await page.locator('html').getAttribute('lang') === language, `${language}: html lang mismatch`);

    const state = await pageState(page);
    assert(state.overflow <= 1, `${language}: horizontal overflow ${state.overflow}px`);
    assert(state.heroWidth > 500 && state.heroHeight > 300, `${language}: hero geometry collapsed`);
    assert(state.h1Size >= 48, `${language}: hero typography unexpectedly small (${state.h1Size}px)`);
    assert(state.focusCount === 4, `${language}: expected four Current Focus items`);
    assert(state.teamCount === 2, `${language}: expected two founder profiles`);
    assert(state.brandLoaded, `${language}: SVG brand mark failed to render`);
    assert(/^20\d{2}$/.test(state.currentYear), `${language}: dynamic footer year was not populated`);
    assert(errors.length === 0, `${language}: browser console/page errors: ${errors.join(' | ')}`);

    await validateSkipLink(page, language);

    await page.locator('#focus').scrollIntoViewIfNeeded();
    await page.waitForFunction(() => {
      const nav = document.querySelector('.nav');
      const focusLink = document.querySelector('.nav-links a[href="#focus"]');
      return nav?.classList.contains('is-compact') && focusLink?.getAttribute('aria-current') === 'location';
    }, null, { timeout: 2500 });

    await validateFounderImages(page, language);
    assert(errors.length === 0, `${language}: browser console/page errors after lazy image load: ${errors.join(' | ')}`);
    await sleep(100);
    await page.screenshot({
      path: path.join(screenshotDir, `${browserName}-${language}-desktop.png`),
      fullPage: false
    });
    rows.push([browserName, language, 'desktop', 'PASS']);
  } catch (error) {
    failures.push(`${browserName}/${language}/desktop: ${error.message}`);
    rows.push([browserName, language, 'desktop', 'FAIL']);
    await page.screenshot({
      path: path.join(screenshotDir, `${browserName}-${language}-desktop-failure.png`),
      fullPage: true
    }).catch(() => {});
  } finally {
    await context.close();
  }
}

async function validateMobile(browserName, browser, language) {
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    hasTouch: true,
    reducedMotion: 'reduce'
  });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', err => errors.push(String(err)));
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });

  try {
    const response = await page.goto(`${base}/${language}/`, { waitUntil: 'networkidle' });
    assert(response && response.status() === 200, `${language}: expected HTTP 200`);

    const state = await pageState(page);
    assert(state.overflow <= 1, `${language}: mobile horizontal overflow ${state.overflow}px`);
    assert(state.brandLoaded, `${language}: mobile SVG brand mark failed to render`);
    assert(errors.length === 0, `${language}: browser console/page errors: ${errors.join(' | ')}`);

    const toggle = page.locator('.mobile-menu-toggle');
    await toggle.waitFor({ state: 'visible' });
    assert(await toggle.getAttribute('aria-expanded') === 'false', `${language}: mobile menu should start closed`);
    await toggle.click();
    assert(await toggle.getAttribute('aria-expanded') === 'true', `${language}: mobile menu did not open`);

    const menu = page.locator('#mobile-navigation');
    assert(await menu.isVisible(), `${language}: mobile navigation is not visible after opening`);
    const focusedHref = await page.evaluate(() => document.activeElement?.getAttribute('href') || '');
    assert(focusedHref.startsWith('#'), `${language}: opening mobile navigation should focus its first section link`);

    await page.locator('#mobile-navigation a[href="#team"]').click();
    await page.waitForFunction(() => {
      const toggle = document.querySelector('.mobile-menu-toggle');
      const menu = document.querySelector('#mobile-navigation');
      return toggle?.getAttribute('aria-expanded') === 'false' && Boolean(menu?.hidden);
    }, null, { timeout: 2500 });

    await toggle.click();
    await page.keyboard.press('Escape');
    assert(await toggle.getAttribute('aria-expanded') === 'false', `${language}: Escape did not close mobile menu`);
    const restored = await page.evaluate(() => document.activeElement?.classList.contains('mobile-menu-toggle') || false);
    assert(restored, `${language}: Escape did not restore focus to the mobile toggle`);

    const reducedState = await page.evaluate(() => {
      const durations = value => value.split(',').map(x => x.trim());
      const navDurations = durations(getComputedStyle(document.querySelector('.nav')).transitionDuration);
      const buttonDurations = durations(getComputedStyle(document.querySelector('.btn')).transitionDuration);
      return {
        heroAnimation: getComputedStyle(document.querySelector('.hero-main'), '::before').animationName,
        navReduced: navDurations.every(value => value === '0s'),
        buttonReduced: buttonDurations.every(value => value === '0s')
      };
    });
    assert(reducedState.heroAnimation === 'none', `${language}: reduced-motion hero animation still active`);
    assert(reducedState.navReduced, `${language}: reduced-motion nav transition still active`);
    assert(reducedState.buttonReduced, `${language}: reduced-motion button transition still active`);

    await validateFounderImages(page, language);
    assert(errors.length === 0, `${language}: browser console/page errors after lazy image load: ${errors.join(' | ')}`);
    await sleep(100);
    await page.screenshot({
      path: path.join(screenshotDir, `${browserName}-${language}-mobile.png`),
      fullPage: false
    });
    rows.push([browserName, language, 'mobile-touch', 'PASS']);
  } catch (error) {
    failures.push(`${browserName}/${language}/mobile: ${error.message}`);
    rows.push([browserName, language, 'mobile-touch', 'FAIL']);
    await page.screenshot({
      path: path.join(screenshotDir, `${browserName}-${language}-mobile-failure.png`),
      fullPage: true
    }).catch(() => {});
  } finally {
    await context.close();
  }
}

async function validate404(browserName, browser) {
  const context = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const page = await context.newPage();
  try {
    const response = await page.goto(`${base}/404.html`, { waitUntil: 'networkidle' });
    assert(response && response.status() === 200, 'local 404 fixture should render');
    const state = await page.evaluate(() => ({
      robots: document.querySelector('meta[name="robots"]')?.content || '',
      h1: document.querySelector('h1')?.textContent?.trim() || '',
      overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      en: Boolean(document.querySelector('a[href="/en/"]')),
      tr: Boolean(document.querySelector('a[href="/tr/"]'))
    }));
    assert(state.robots.toLowerCase().includes('noindex'), '404 fixture must remain noindex');
    assert(state.h1 === 'Page not found.', '404 heading changed unexpectedly');
    assert(state.overflow <= 1, `404 horizontal overflow ${state.overflow}px`);
    assert(state.en && state.tr, '404 language recovery links missing');
    rows.push([browserName, 'n/a', '404-mobile', 'PASS']);
  } catch (error) {
    failures.push(`${browserName}/404: ${error.message}`);
    rows.push([browserName, 'n/a', '404-mobile', 'FAIL']);
  } finally {
    await context.close();
  }
}

async function main() {
  for (const [browserName, browserType] of Object.entries(browserTypes)) {
    const browser = await browserType.launch({ headless: true });
    try {
      for (const language of ['en', 'tr']) {
        await validateDesktop(browserName, browser, language);
        await validateMobile(browserName, browser, language);
      }
      await validate404(browserName, browser);
    } finally {
      await browser.close();
    }
  }

  const header = '| Browser | Language | Profile | Result |';
  const divider = '| --- | --- | --- | --- |';
  const lines = rows.map(row => `| ${row.join(' | ')} |`);
  const failureLines = failures.length ? ['', '## Failures', '', ...failures.map(x => `- ${x}`)] : [];
  const markdown = ['# Cross-browser device QA', '', header, divider, ...lines, ...failureLines, ''].join('\n');
  fs.writeFileSync(path.join(outputDir, 'summary.md'), markdown);
  if (process.env.GITHUB_STEP_SUMMARY) fs.appendFileSync(process.env.GITHUB_STEP_SUMMARY, markdown);
  console.log(markdown);

  if (failures.length) process.exit(1);
}

main().catch(error => {
  console.error(error);
  process.exit(1);
});
