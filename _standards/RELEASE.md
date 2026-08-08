# Releasing a plugin

A checklist for the human doing it, in order. **It is not the whole procedure.**

The exhaustive version and metadata pre-flight — the header order, the twenty-odd
invariants, the tagging — lives in the `release-wp-plugin` skill and is not
repeated here. What is here is the sequence, and the three things the skill does
not cover: **CI**, **the block build**, and **`assets/`**.

Nothing in this repository releases anything. Every step below that touches SVN
is yours.

---

## 1. Before anything

- [ ] **`git fetch` first.** A remote can be ahead of your checkout, and this has
      happened: `git status` says nothing about it without the fetch.
- [ ] `python3 bin/verify.py <plugin>` is **0 failing**.
- [ ] **CI is green on the commit you are about to ship**, not on some earlier
      one:
      ```sh
      gh -R lesterchan/<plugin> run list --workflow=ci.yml --event=push --limit 1 \
        --json conclusion,headSha
      ```
      Check the `headSha` against your local `HEAD`. A green run on the wrong
      commit is not a green run.
- [ ] **A green `verify.py` is not evidence the suites pass.** The two enforce
      overlapping rules from separate sources — the canonical README section
      list, for one, lives in both `bin/verify.py` and the shared metadata
      fixture. CI is what proves the suites.
- [ ] Nothing unpushed, nothing dirty.

## 2. If the plugin has blocks

Eight do. Anything with a `src/` directory.

- [ ] `bin/build` succeeds. The deploy runs it and now **aborts if it fails** —
      it did not always, and a silent failure shipped whatever `build/` happened
      to be on disk.
- [ ] Remember what ships: **`build/` yes, `src/` no.** `build/` is gitignored,
      so `git status` will never mention the thing that reaches users.

## 3. The pre-flight

Run the `release-wp-plugin` skill. It checks the stable tag against the header
version and the version constant, the changelog entry, the header order, the
`index.php` guards, the LICENSE, the https links, and the rest.

- [ ] All PASS.
- [ ] The tag does not already exist on wordpress.org.

## 4. Deploy trunk

```sh
bin/plugin_deploy.sh <plugin>
```

- [ ] **Read the `svn stat` output it prints.** The script runs `svn stat` and
      `svn ci` in one uninterrupted pass, so there is no pause to approve — by
      the time you see the list it is published.
- [ ] The real gate is the `git diff` of what you changed, read **before** you
      run this.

## 5. `assets/` — separate, manual, and easy to forget

The skill does not touch these. They are not part of `trunk/`, so nothing
automates them, and the deploy will not mention them.

- [ ] `svn status assets` in the plugin's SVN checkout.
- [ ] **`!` is not `D`.** A missing file is *not* staged for deletion, and
      `svn commit` will skip it — the old image stays live. Removing one takes
      `svn delete --force`.
- [ ] `svn add` anything showing `?`.
- [ ] **Count the screenshots against the README.** wordpress.org captions by
      *position*: `screenshot-N.png` gets the Nth line of `## Screenshots`. More
      files than lines means the extras render with no caption; fewer means the
      captions describe the wrong pictures.
- [ ] Commit `assets/`.

## 6. Tag

Per the skill: `svn copy` trunk to `tags/<version>`, straight to the live
repository.

## 7. Afterwards

- [ ] Open the wordpress.org plugin page and look at it. The Installation tab,
      the screenshots and their captions, and the changelog are the parts no
      check validates — **four separate defects this year were found by a person
      looking at a picture and none by any test.**

---

## Two things that have gone wrong before

**A stale screenshot outliving its caption.** The recapture thinned ten plugins'
screenshot sets, and the old files stayed versioned in SVN as `!`. Committing in
that state leaves wordpress.org serving images the README no longer describes.

**Something untracked but present on disk shipping.** The deploy rsyncs the
**working tree**, not a clean export. That is how Playwright's `artifacts/`
reached wordpress.org with a logged-in session cookie in it. The exclusion list
in `bin/plugin_deploy.sh` is the only thing standing between your disk and a
release; when a plugin grows a new kind of generated directory, that list needs
a new line **before** the first release that has one.
