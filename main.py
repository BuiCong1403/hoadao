name: Update TV M3U

on:
  schedule:
    - cron: '0 */3 * * *'   # ⏰ mỗi 3 giờ
  workflow_dispatch:

permissions:
  contents: write

jobs:
  update:
    runs-on: ubuntu-latest
    timeout-minutes: 5

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install
        run: pip install requests

      - name: Run script
        run: python main.py   # đổi nếu tên file khác

      - name: Commit
        run: |
          git config --global user.name "github-actions"
          git config --global user.email "actions@github.com"

          git add hoadaotv.m3u

          git diff --cached --quiet || git commit -m "update tv m3u (3h)"

          git push
