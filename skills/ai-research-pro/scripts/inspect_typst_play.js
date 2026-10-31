const { chromium } = require('/home/tontonyuta/clinical-ward/node_modules/playwright');

async function inspectTypstPlay() {
  console.log('🚀 Inspecting https://typst.app/play/ with Playwright...');
  const browser = await chromium.launch({
    executablePath: '/home/tontonyuta/.local/bin/google-chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  const wasmRequests = [];

  page.on('request', req => {
    const url = req.url();
    if (url.includes('.wasm') || url.includes('typst') || url.includes('compile')) {
      wasmRequests.push({ url, method: req.method(), resourceType: req.resourceType() });
    }
  });

  try {
    await page.goto('https://typst.app/play/', { waitUntil: 'networkidle', timeout: 30000 });
    console.log('✅ Loaded typst.app/play/! Title:', await page.title());
    console.log('Wasm / Typst requests detected:');
    console.log(JSON.stringify(wasmRequests.slice(0, 10), null, 2));

    // Evaluate how it renders
    const info = await page.evaluate(() => {
      const canvas = document.querySelector('canvas');
      const svg = document.querySelector('svg');
      const editor = document.querySelector('.cm-editor') || document.querySelector('.monaco-editor') || document.querySelector('textarea');
      return {
        hasCanvas: !!canvas,
        hasSvg: !!svg,
        editorType: editor ? editor.className : 'unknown',
        scripts: Array.from(document.querySelectorAll('script')).map(s => s.src).filter(Boolean)
      };
    });

    console.log('DOM Evaluation:', info);
  } catch (err) {
    console.error('Error inspecting typst.app/play/:', err.message);
  } finally {
    await browser.close();
  }
}

inspectTypstPlay().catch(console.error);
