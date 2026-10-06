# roles.tsv（第1版）から第2版の役割表を作る：直した聞き役の行の文と役割を差し替える
NEW = {
 'c511': ('まとめ', 'その柱に、水が集まっていたんだね。'),
 'c514': ('まとめ', 'まわりの柱に、重さが回っていったんだね。'),
 'c617': ('まとめ', '崩れる直前に、沈み方が速くなったんだね。'),
 'c620': ('まとめ', '東の部分も、下の階の柱から崩れたんだね。'),
 'c714': ('まとめ', '見つかるまで、長くかかったんだね。'),
 'c814': ('まとめ', '実物に近い物を造って、壊して確かめたんだね。'),
 'ca09': ('まとめ', '試験の継ぎ目は、強さを失ったんだね。'),
 'cb01': ('質問', 'たとえば、となりの工事のせいだという話は？'),
 'cc07': ('質問', 'まわりの町では、何か動きはあったの？'),
 'cc15': ('反応', '決まりが、ずいぶん細かくなったね。'),
 'c622': (None, 'あの夜だけで、全部が起きたわけじゃないんだね。'),
}
R = 'C:/Users/konar/Desktop/zukai-engine/ref/ep19/'
out, done = [], set()
for ln in open(R + 'v1_build/roles.tsv', encoding='utf-8').read().split('\n'):
    c = ln.split('\t')[0]
    if c in NEW:
        r, t = NEW[c]
        r = r or ln.split('\t')[1]  # 役割はそのまま・文だけ替える
        out.append('\t'.join((c, r, t))); done.add(c)
    elif ln.startswith('#'):
        out.append(ln.replace('第1版', '第2版（④\' で聞き役の11行を直した）'))
    else:
        out.append(ln)
assert done == set(NEW), set(NEW) - done
v2 = open(R + 'daihon_v2.md', encoding='utf-8').read()
for c, (r, t) in NEW.items():
    assert ('> Q: ' + t) in v2, c
open(R + 'v2_build/roles_v2.tsv', 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
print('ok', len(out))
