# ClustIce

An ongoing project.


[x] 分極の最適化.(オプションでいい)←ランダム方式にした。
[ ] constellationの高速化。表面にあるはずの、欠陥ノード間の距離で外形を作り、距離1の結合で内部を作る。あとは捨てる、というのでどうだ? これは過去に事例がありそう。
[ ] すべての可能な配向を列挙したい。そのために、まずice ruleを満たすすべての配置を高速に無駄なく生成する必要がある。Hamilton環路を描く方法でできそうな気はする。
  * hamilton経路を探す。
  * それに沿って、矢印を→←→←のように交互に指定する。
  * 残りの矢印は自ずと配向が定まる。
  * いやだめだ。最初の経路に偶奇性がある。残る矢印が偶同士をつなぐと向きが定まらない。



まだしばらくpypiには上げない。インストールはgithubから行ってもらう。
