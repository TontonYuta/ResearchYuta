const { chromium } = require('/home/tontonyuta/clinical-ward/node_modules/playwright');
const fs = require('fs');

async function searchTypstApps() {
  console.log('🚀 Searching GitHub for Typst Apps and Tools via Playwright...');
  const browser = await chromium.launch({
    executablePath: '/home/tontonyuta/.local/bin/google-chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  const searchQueries = [
    'https://github.com/topics/typst',
    'https://github.com/Myriad-Dreamin/shiroa',
    'https://github.com/typst/typst/discussions/categories/show-and-tell',
    'https://github.com/badagames/typst-live',
    'https://github.com/lucperkins/typst-docgen'
  ];

  const results = {};

  for (const url of searchQueries) {
    try {
      console.log(`🔍 Crawling: ${url}...`);
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 });
      
      const pageInfo = await page.evaluate(() => {
        const title = document.title;
        const mainText = document.querySelector('main')?.innerText?.slice(0, 2500) || '';
        return { title, mainText };
      });
      results[url] = pageInfo;
      console.log(`✅ Fetched: ${pageInfo.title}`);
    } catch (e) {
      console.error(`Error on ${url}:`, e.message);
    }
  }

  await browser.close();

  fs.writeFileSync(
    '/home/tontonyuta/.gemini/antigravity-cli/brain/29d456f4-f165-40c3-8cf0-9389f16f65ec/scratch/crawled_typst_apps.json',
    JSON.stringify(results, null, 2),
    'utf-8'
  );
  console.log('💾 Done saving search results!');
}

searchTypstApps().catch(console.error);
