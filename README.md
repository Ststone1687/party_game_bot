# party_game_bot

這是一個因為晚上11點有些人可能會太閒沒事做，於是所以製作的遊戲機器人，主要是將市面上一些常見的Party Game類型的桌遊以文字的方式搬到Discord上面遊玩。

[遊戲Discord群組](https://discord.gg/k3WaMK9Apj)

---

## 遊戲種類

1.	電車難題
2.	唬爛王（開發中）

---

## 安裝方式

clone本專案`git clone https://github.com/Ststone1687/party_game_bot.git`。

`pip install discord.py`。

於discord官網申請機器人並獲得`Token`，邀請至discord群組。

將`Token`放入`token.txt`中。

將要遊玩的遊戲檔案`.py`檔放入`cmds`資料夾中。

執行`main.py`。

請自行修改遊戲中私有頻道相關程式碼，目前此部分還在開發，更加簡易操作的介面將在未來開發。

---

### 電車難題

一輛失控的列車在鐵軌上行駛。有兩個軌道可以運行，在這兩個軌道上分別有著不同的人物，有兩位玩家擔任辯護者，他們的目的都是要陷害，讓電車最終輾過另一方，而使己方倖存下來。
而其他玩家則會投票決定最終電車的去向。當然他們不是無憑無據地辯護，他們會獲得形容詞牌，用以更詳細描述己方及對方的身分、立場。

遊戲人數需求：三人以上

相關指令：

```
1.!重置遊戲(reset)：有主持人身分組的話可以用來重置遊戲。
2.!加入遊戲(join)：用來加入遊戲。
3.!開始遊戲(start)：有主持人身分組的話可以用來開始遊戲。
4.!比賽狀況(information)：可以看到當前的比賽狀況。
5.!公布結果(result)：有主持人身分組且所有人都投完票的話可以查看投票結果。
6.!投票(vote) [A或B]:投票決定應該讓火車壓死A或是B，只有非比賽中的人可以投票。
7.!查看手牌(cards)：比賽中的人可以用來查看自己的手牌。
8.!出牌(use) [卡片編號] [A或B]：選擇一張卡片對A鐵軌或B鐵軌的人用。
9.!分數(score)：看目前的總得分。
10.!排位(rating)：看目前的排位資訊。
11.!查看角色(characters)：看有哪些人是你可以保護的（你是小孩子，不能選擇全都要）。
12.!保護(protect) [編號]：決定要保護誰，不能更改。
```

實際遊戲畫面截圖：

![image](https://user-images.githubusercontent.com/60891434/229156756-01dbaca0-6f3d-4cd7-a4c4-54c257766b8d.png)

![image](https://user-images.githubusercontent.com/60891434/229157918-167f239a-5f56-4aaa-9f32-e075959b2819.png)


