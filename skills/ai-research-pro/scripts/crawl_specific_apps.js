const { chromium } = require('/home/tontonyuta/clinical-ward/node_modules/playwright');

async function crawlSpecificApps() {
  const browser = await chromium.launch({
    executablePath: '/home/tontonyuta/.local/bin/google-chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  const urls = [
    'https://github.com/rendercv/rendercv',
    'https://github.com/vnotex/vnote',
    'https://github.com/mush42/typesetter'
  ];

  for (const url of urls) {
    try {
      console.log(`Checking ${url}...`);
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
      const info = await page.evaluate(() => {
        const title = document.title;
        const snippet = document.querySelector('article.markdown-body')?.innerText?.slice(0, 1000) || '';
        return { title, snippet };
      });
      console.log(`✅ ${info.title}`);
      console.log(info.snippet.slice(0, 200) + '...\n');
    } catch (e) {
      console.log(`Error on ${url}:`, e.message);
    }
  }

  await browser.close();
}

crawlSpecificApps().catch(console.error);
