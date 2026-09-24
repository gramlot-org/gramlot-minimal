# 010 · Usage

Document ID: **GS-010**.

<a id="gs-010-005"></a>
## 005 · Build

Install local core, NodeJS, standalone and Hello World npm archives in a consumer
directory. From there run:

```sh
npx --no-install gramlot-standalone build node_modules/gramlot-example-app/js/pages/index.js -o dist/hello-world.html
```

The command takes exactly one .js or .mjs page and an .html/.htm output. It does not
read the old TOML project format. Paths resolve against the current directory.
Failed builds do not replace an existing output; successful writes are atomic.

<a id="gs-010-010"></a>
## 010 · Author a page

```javascript
import {Page as BasePage, source} from '@gramlot/native-html/page';
export class Page extends BasePage {
    main(root) { root.h1('Hello'); root.section(null, {id:'details'}); }
    details(root, {text}) { root.p(text); }
}
source(Page.prototype.details);
```

Page.main is executed when the HTML opens, not when building. Runtime transport
is owned by Gramlot. There is no additional standalone Page subclass.

<a id="gs-010-015"></a>
## 015 · Open and close

Open the output from disk. globalThis.gramlot is the started instance; its normal
Source APIs and remoteSource operate without a server. dispose terminates its Worker.
Runtime startup errors are reported to the browser console. No database is included.

<a id="gs-010-020"></a>
