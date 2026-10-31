const { chromium } = require('/home/tontonyuta/clinical-ward/node_modules/playwright');
const fs = require('fs');

async function crawlAwesomeTypst() {
  console.log('🚀 Crawling awesome-typst with Playwright...');
  const browser = await chromium.launch({
    executablePath: '/home/tontonyuta/.local/bin/google-chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.goto('https://github.com/qjcg/awesome-typst', { waitUntil: 'domcontentloaded', timeout: 30000 });

  const content = await page.evaluate(() => {
    const readme = document.querySelector('article.markdown-body');
    if (!readme) return '';
    // Find headings related to Apps, Editors, Tools
    return readme.innerText;
  });

  await browser.close();

  fs.writeFileSync(
    '/home/tontonyuta/.gemini/antigravity-cli/brain/29d456f4-f165-40c3-8cf0-9389f16f65ec/scratch/awesome_typst.txt',
    content,
    'utf-8'
  );
  console.log('💾 Saved awesome-typst content, length: ' + content.length);
}

crawlAwesomeTypst().catch(console.error);
