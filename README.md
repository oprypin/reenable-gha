## Automatically re-enable GitHub Actions scheduled workflows

If you're maintaining multiple stable projects, you might have noticed that GitHub simply disables scheduled workflows after seeing no commits for some time. Well, this script won't let it do that if you run it on a schedule. It bumps the expiration date of all your workflows that mention a schedule.

## Base instructions

* Create a token with `repo`, `workflow` at https://github.com/settings/tokens
  * Export it as the environment variable `GITHUB_TOKEN`
* Run `python3 reenable.py`.
  * Figure out how to schedule it monthly.

## Meta automation

* Fork this repo!
* Create a personal token with `repo`, `workflow` at https://github.com/settings/tokens
  * Add it as a repository secret (name `PERSONAL_TOKEN`) at https://github.com/[username]/reenable-gha/settings/secrets/actions/new
* Make sure that Actions are enabled in the fork.

## Self-hosted automation with systemd

* Create a token with `repo`, `workflow` at https://github.com/settings/tokens
  * Paste it into the file *reenable-gha.service* instead of the asterisks.
* Put the script *reenable.py* into a known absolute path
  * Change *reenable-gha.service* to refer to it instead of the placeholder.
* Put *reenable-gha.service*, *reenable-gha.timer* into */etc/systemd/system*.
* Run `sudo systemctl daemon-reload; sudo systemctl enable --now reenable-gha.timer`.
  * Also run `sudo systemctl start reenable-gha` to activate it immediately.
  * Run `journalctl -u reenable-gha` to watch progress.
