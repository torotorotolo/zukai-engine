#!/usr/bin/env bash
# 25本目 映像方針：公的な機関のファイルを取る（10-25 カズヤくん「公的な機関のファイルは許可不要」）。
#   bash ref/ep25/eizou_build/fetch_pub25.sh <置き場（ref/ep25/src/ の下）> <記号> <URL> [<記号> <URL> ...]
# 手順＝HEAD で大きさ → GET → 大きさが HEAD と合うか → md5 を2回（落としかけを測らない）→ src/fetch_log.tsv に1行。
# 名乗り（User-Agent）にメールや @ を入れない。会社・Commons・フリー素材・報道はこの道具で取らない（了承②のあと fetch25 系で）。
set -u
SRC="$(cd "$(dirname "$0")/../src" && pwd)"
DEST="$SRC/$1"; shift
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) research-fetch"
mkdir -p "$DEST"
LOG="$SRC/fetch_log.tsv"
echo "# $(date '+%Y-%m-%d %H:%M:%S') eizou_build/fetch_pub25.sh" >> "$LOG"
ng=0
while [ $# -ge 2 ]; do
  key="$1"; url="$2"; shift 2
  fn="$DEST/$(basename "${url%%\?*}")"
  cl=$(curl -sI -A "$UA" -L "$url" | tr -d '\r' | awk -F': ' 'tolower($1)=="content-length"{v=$2} END{print v}')
  code=$(curl -s -A "$UA" -L -o "$fn" -w "%{http_code}" "$url")
  sz=$(wc -c < "$fn" | tr -d ' ')
  m1=$(md5sum "$fn" | cut -d' ' -f1); sleep 1; m2=$(md5sum "$fn" | cut -d' ' -f1)
  st=OK
  [ "$code" = "200" ] || st="NG(http $code)"
  [ -n "$cl" ] && [ "$cl" != "$sz" ] && st="NG(大きさ HEAD $cl ≠ $sz)"
  [ "$m1" = "$m2" ] || st="NG(md5 が2回で違う)"
  [ "$st" = OK ] || ng=$((ng+1))
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$key" "${fn#$SRC/}" "get(映像方針)" "$cl" "$sz" "$m1" "$url" >> "$LOG"
  echo "$st $key $sz bytes md5=$m1 ${fn#$SRC/}"
  sleep 2
done
echo "NG=$ng"
exit $ng
