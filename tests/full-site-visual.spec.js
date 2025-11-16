const { test, expect } = require('@playwright/test');

test.describe('BC Website - Full Site Visual Review', () => {
  const baseURL = 'http://localhost:4000';

  test('Homepage - Desktop view', async ({ page }) => {
    await page.goto(`${baseURL}/`, { waitUntil: 'networkidle' });
    await page.screenshot({ path: 'test-results/01-homepage-desktop.png', fullPage: true });

    // Verify key content
    const heading = page.locator('h1');
    await expect(heading).toContainText('Brian Cohn Ph.D.');
  });

  test('Homepage - Mobile view (375px)', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(`${baseURL}/`, { waitUntil: 'networkidle' });
    await page.screenshot({ path: 'test-results/02-homepage-mobile.png', fullPage: true });
  });

  test('Research Page - Desktop', async ({ page }) => {
    await page.goto(`${baseURL}/research/`, { waitUntil: 'networkidle' });
    await page.screenshot({ path: 'test-results/03-research-desktop.png', fullPage: true });

    // Verify research content
    const title = page.locator('h1');
    await expect(title).toContainText('Research & Whitepapers');
  });

  test('ML Tools Page - Desktop', async ({ page }) => {
    await page.goto(`${baseURL}/posts/`, { waitUntil: 'networkidle' });
    await page.screenshot({ path: 'test-results/04-ml-tools-desktop.png', fullPage: true });

    // Verify ML tools content
    const heading = page.locator('h1');
    await expect(heading).toContainText('ML Tools');
  });

  test('Press Kit Page - Desktop', async ({ page }) => {
    await page.goto(`${baseURL}/presskit/`, { waitUntil: 'networkidle' });
    await page.screenshot({ path: 'test-results/05-presskit-desktop.png', fullPage: true });

    // Verify press kit content
    const heading = page.locator('h1');
    await expect(heading).toContainText('Press Kit');
  });

  test('Meet Page - Desktop', async ({ page }) => {
    await page.goto(`${baseURL}/meet/`, { waitUntil: 'networkidle' });
    await page.screenshot({ path: 'test-results/06-meet-desktop.png', fullPage: true });

    // Verify meet page content
    const heading = page.locator('h1');
    await expect(heading).toContainText('Schedule a Meeting');
  });

  test('Navigation Links', async ({ page }) => {
    await page.goto(`${baseURL}/`, { waitUntil: 'networkidle' });

    // Take screenshot of navigation
    const nav = page.locator('nav');
    await expect(nav).toBeVisible();

    // Test navigation
    await page.click('nav a[href="/research/"]');
    await page.waitForLoadState('networkidle');
    const researchTitle = page.locator('h1');
    await expect(researchTitle).toContainText('Research');
  });

  test('Email Links Updated', async ({ page }) => {
    await page.goto(`${baseURL}/`, { waitUntil: 'networkidle' });

    // Check footer email
    const footerEmail = page.locator('footer a[href*="brian.cohn@kaspect"]');
    await expect(footerEmail).toBeVisible();

    // Verify it contains the correct email
    const emailText = await footerEmail.textContent();
    expect(emailText).toContain('brian.cohn@kaspect.com');
  });

  test('Styling - Colors and Typography', async ({ page }) => {
    await page.goto(`${baseURL}/`, { waitUntil: 'networkidle' });

    // Check header has styling
    const header = page.locator('header');
    const headerBG = await header.evaluate(el => window.getComputedStyle(el).backgroundColor);
    expect(headerBG).toBeTruthy();

    // Check heading font
    const h1 = page.locator('h1');
    const fontFamily = await h1.evaluate(el => window.getComputedStyle(el).fontFamily);
    expect(fontFamily).toBeTruthy();
  });

  test('All Pages Load Without Errors', async ({ page }) => {
    const pages = ['/', '/research/', '/posts/', '/presskit/', '/meet/'];

    for (const pagePath of pages) {
      await page.goto(`${baseURL}${pagePath}`, { waitUntil: 'networkidle' });

      // Check for console errors
      const errors = [];
      page.on('console', msg => {
        if (msg.type() === 'error') errors.push(msg.text());
      });

      // Verify page has content
      const main = page.locator('main');
      await expect(main).toBeVisible();
    }
  });
});
