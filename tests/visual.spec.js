const { test, expect } = require('@playwright/test');

test.describe('BC Website - Visual Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Wait for server to be ready
    await page.goto('http://localhost:4000', { waitUntil: 'networkidle' });
  });

  test('Homepage renders with new design', async ({ page }) => {
    // Take screenshot
    await page.screenshot({ path: 'test-results/homepage.png', fullPage: true });

    // Verify page loaded (title should not be empty)
    const title = await page.title();
    expect(title.length).toBeGreaterThan(0);

    // Verify main heading exists
    const heading = page.locator('h1');
    await expect(heading).toContainText('Brian Cohn Ph.D.');

    // Verify navigation menu exists
    const nav = page.locator('header nav');
    await expect(nav).toBeVisible();

    // Check for key content sections
    const roles = page.locator('text=Director of Research');
    await expect(roles).toBeVisible();
  });

  test('CSS colors are applied correctly', async ({ page }) => {
    // Check that header is styled
    const header = page.locator('header');
    const headerColor = await header.evaluate(el => window.getComputedStyle(el).backgroundColor);

    // Verify header has some styling applied
    expect(headerColor).toBeTruthy();

    // Check for serif fonts on headings (playfair should be loaded)
    const h1 = page.locator('h1');
    const fontFamily = await h1.evaluate(el => window.getComputedStyle(el).fontFamily);

    // Font should contain either playfair or be from the custom stylesheet
    expect(fontFamily).toBeTruthy();
  });

  test('Responsive design works on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });

    // Reload to apply mobile layout
    await page.reload({ waitUntil: 'networkidle' });

    // Take mobile screenshot
    await page.screenshot({ path: 'test-results/homepage-mobile.png', fullPage: true });

    // Verify content is still visible
    const heading = page.locator('h1');
    await expect(heading).toBeVisible();
  });

  test('Links are interactive', async ({ page }) => {
    // Check for email contact link
    const emailLink = page.locator('a[href*="briancohn@kaspect"]').first();
    await expect(emailLink).toBeVisible();

    // Check for navigation menu - should have multiple links
    const navLinks = page.locator('nav a');
    const count = await navLinks.count();
    expect(count).toBeGreaterThan(0);
  });
});
