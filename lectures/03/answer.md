# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
- `--trace` で見えたツール呼び出し（ツール名と引数）：
- 1つの質問での LLM 呼び出し回数（`requests`）：
- 追加したツールと、docstring に書いた説明：

## 宿題

- 取り組んだレベル：基礎
- やったこと：
app/agent.py の INSTRUCTIONS と、app/tools.py の search_glossary のdocstringを変更し、同じ質問に対するツール呼び出しと回答の変化を比較した。
質問は、すべて以下に統一した。
「LoRA と QLoRA の違いは？」
比較条件は次の3ケースとした。

Case 0（変更前）：元のINSTRUCTIONSとdocstringを使用。
Case 1（INSTRUCTIONS変更）：「必ずsearch_glossaryで用語集を確認する」という指示を削除。
Case 2（docstring変更）：INSTRUCTIONSを元に戻し、検索用語を「1つだけ入れる」から「複数の用語をまとめて入れてよい」に変更。

変更する箇所を1か所ずつに限定し、それぞれ --trace を付けて実行した。

- 結果：
Case 0：変更前
[tool call] search_glossary({'query': 'LoRA'})
[tool call] search_glossary({'query': 'QLoRA'})
2つの用語を個別に検索し、用語集の内容に基づいて違いを説明した。

Case 1：INSTRUCTIONS変更
[tool call] search_glossary({'query': 'LoRA'})
[tool call] search_glossary({'query': 'QLoRA'})
検索を必須とする指示を削除したが、変更前と同じく2回の検索が実行された。
回答内容についても、大きな違いは見られなかった。

Case 2：docstring変更
[tool call] search_glossary({'query': 'LoRA QLoRA'})
2つの用語をまとめて検索するようになり、ツール呼び出し回数が2回から1回に減少した。
同じ条件で再実行した場合も、2つの用語をまとめて検索する動作が確認できた。
一方、LLMの呼び出し回数は2回のままであった。
また、最終回答では引き続きLoRAとQLoRAの違いが説明されたが、--trace のツール返却内容は省略表示されているため、両方の定義が取得されたかについては追加確認が必要である。

- 気づき・疑問：
今回の比較では、INSTRUCTIONSから検索を必須とする指示を削除しても、検索の実行方法は変わらなかった。
これは、ツール側のdocstringにも検索を促す説明が残っていたためではないかと考えられる。
一方、docstringを変更すると、ツールの実装自体は変えていないにもかかわらず、モデルが複数の用語をまとめて検索するようになった。
この結果から、ツールの説明文が、モデルによるツールの選択だけでなく、引数の指定方法にも影響することが確認できた。