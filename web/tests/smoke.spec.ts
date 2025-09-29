import { test, expect } from '@playwright/test';

const BASE = process.env.WEB_BASE_URL || 'http://localhost:5173';

test('loads app and navigates to Receipts', async ({ page }) => {
  await page.goto(BASE);
  await expect(page.getByRole('heading', { name: 'RainRef' })).toBeVisible();
  await page.getByRole('link', { name: 'Receipts' }).click();
  await expect(page.getByRole('heading', { name: 'Receipts' })).toBeVisible();
});


