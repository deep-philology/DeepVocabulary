/*
 * This script will eventually overtake npm run dev, but for now
 * it handles the browser-sync config.
 *
 * At this point the only required options not suitable with CLI is
 * the proxy.proxyOptions.xfwd (needed for proper OIDC)
**/

const ev = require('envalid');
const bs = require('browser-sync').create();

const env = ev.cleanEnv(process.env, {
  FE_PORT: ev.port({ default: 3000 }),
  BE_PORT: ev.port({ default: 8000 }),
});

bs.init({
  open: false,
  port: env.FE_PORT,
  proxy: {
    target: `http://localhost:${env.BE_PORT}`,
    proxyOptions: {
      xfwd: true,
    },
  },
  files: [
    'static/dist/js/*.js',
    'static/dist/css/*.css',
  ],
});
