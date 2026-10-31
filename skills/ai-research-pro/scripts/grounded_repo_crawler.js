const { chromium } = require('/home/tontonyuta/clinical-ward/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const TARGET_REPOS = [
  'typst/typst',
  'Myriad-Dreamin/tinymist',
  'Myriad-Dreamin/typst.ts',
  'Enter-tainer/typst-preview',
  'typst/packages',
  'cetz-package/cetz',
  'touying-typ/touying',
  'johannes-kuehn/typst-snippets'
];

async function crawlRepos() {
  console.log('🚀 Launching Playwright with system Google Chrome...');
  const browser = await chromium.launch({
    executablePath: '/home/tontonyuta/.local/bin/google-chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });

  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  });

  const results = [];

  for (const repo of TARGET_REPOS) {
    const url = `https://github.com/${repo}`;
    console.log(`\n🔍 [Playwright Grounding] Crawling: ${url}...`);
    const page = await context.newPage();
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 });
      
      const repoData = await page.evaluate(() => {
        const starEl = document.querySelector('#repo-stars-counter-star') || document.querySelector('.js-social-count');
        const stars = starEl ? starEl.innerText.trim() : 'N/A';
        const descEl = document.querySelector('p.f4') || document.querySelector('[itemprop="about"]');
        const description = descEl ? descEl.innerText.trim() : '';
        const topics = Array.from(document.querySelectorAll('.topic-tag')).map(el => el.innerText.trim());
        
        // Grab top of README
        const readmeArticle = document.querySelector('article.markdown-body');
        let readmeSnippet = '';
        if (readmeArticle) {
          readmeSnippet = readmeArticle.innerText.slice(0, 1500).replace(/\n\s*\n/g, '\n');
        }
        
        // Languages
        const langEls = Array.from(document.querySelectorAll('.Layout-sidebar .Progress + ul li'));
        const languages = langEls.map(li => li.innerText.replace(/\s+/g, ' ').trim());

        return {
          stars,
          description,
          topics,
          languages,
          readmeSnippet
        };
      });

      console.log(`✅ Success: ${repo} | Stars: ${repoData.stars} | Langs: ${repoData.languages.slice(0, 2).join(', ')}`);
      results.push({
        repo,
        url,
        ...repoData
      });
    } catch (err) {
      console.error(`❌ Error crawling ${repo}:`, err.message);
    } finally {
      await page.close();
    }
  }

  await browser.close();

  const outDir = '/home/tontonyuta/.gemini/antigravity-cli/brain/29d456f4-f165-40c3-8cf0-9389f16f65ec/scratch';
  fs.mkdirSync(outDir, { recursive: true });
  const outFile = path.join(outDir, 'crawled_typst_repos.json');
  fs.writeFileSync(outFile, JSON.stringify(results, null, 2), 'utf-8');
  console.log(`\n💾 Saved crawled data to: ${outFile}`);
}

crawlRepos().catch(console.error);
