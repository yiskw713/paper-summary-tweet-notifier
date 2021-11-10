# paper summary tweet notifier

論文に関して言及をしている日本語ツイートや特定のアカウントからのツイートを，LINEやslackに通知するアプリです．<br>
GitHub Actionsを使用して，1日に1回通知を行います．<br>


## 概要

![image](https://user-images.githubusercontent.com/38214459/141119314-cfd12484-0593-4efc-802c-62e9c5d97520.png)

本アプリの処理の流れは以下の通りです．

`GitHub Actionによるjob scheduling` -> `Twitter APIを使用したツイートの取得` -> `LINE / slackへの通知`

より詳細な情報に関しては[こちら](https://yiskw713.hatenablog.com/entry/2021/11/10/223848)をご覧ください．


## 使い方

1. このレポジトリをフォークします．
1. フォークしたレポジトリのページで，GitHub Actionsを有効にします
1. [こちらのページ](https://developer.twitter.com/en)からTwitter APIの利用申請を行います
    * 参考ページ: [2021年度版 Twitter API利用申請の例文からAPIキーの取得まで詳しく解説](https://www.itti.jp/web-direction/how-to-apply-for-twitter-api/)
1. 申請が通ったら，Customer Key(API Key), Customer Secret (API Secret), Access Token, Access Secretを取得します．
    * こちらの値は次に使用するので，それぞれメモをとっておいた方が良いです．
1. 取得したkeyとtokenをそれぞれCustomer Keys(API Key)とAccess Tokenを，GitHub Secretsとして登録します
    * レポジトリのページのSettings -> Secretsから登録が行えます．
    * それぞれのkeyとsecretの名前を，以下のようにします．valueは上で取得した値を使用します．
        * Customer Key (API Key) -> `CUSTOMER_KEY`
        * Customer Secret (API Secret) -> `CUSTOMER_SECRET`
        * Access Token -> `ACCESS_TOKEN`
        * Access Secret -> `ACCESS_SECRET`
1. 【LINEに通知したい場合】 LINEのTokenを発行します．
    1. [LINE Notify](https://notify-bot.line.me/ja/)の右上のログインをクリックします
    1. LINEのアカウントログイン情報を入力して，ログインします
    1. 右上の自分のユーザー名のところから，マイページに移動します
    1. マイページで，開発者向けのアクセストークン発行します
    1. GitHubのレポジトリページのSettings -> Secretsにて，`LINE_TOKEN`という名前で発行したトークンを登録します
1. 【slackに通知したい場合】Incoming Webhook URLを取得します
    1. [Slack での Incoming Webhook の利用](https://slack.com/intl/ja-jp/help/articles/115005265063-Slack-%E3%81%A7%E3%81%AE-Incoming-Webhook-%E3%81%AE%E5%88%A9%E7%94%A8)のページを参考に，
    Incoming Webhook URLを取得します．
    1. GitHubのレポジトリページのSettings -> Secretsにて，`SLACK_INCOMING_WEBHOOK_URL`という名前で発行したIncoming Webhook URLを登録します．
1. (任意) ツイートを取得する際のキーワードの設定
    * `src/setting.py`の中に検索したいキーワード(`KEYWORDS`)を設定できます．
    * デフォルトではいくつかの学会，及びarXivのURLが記載されています．
    * `github.com セグメンテーション`といったようなキーワードを追加することで，セグメンテーションと記述されているgithubのレポジトリを引用したツイートを取得することができます．

    ```python
    KEYWORDS = [
        "openaccess.thecvf.com",
        "arxiv.org",
        "ojs.aaai.org",
        "iclr.cc",
        "nips.cc",
        "icml.cc",
        "aclweb.org",
    ]
    ```

1. (任意) ツイートを通知したくないユーザーの設定
    * `src/setting.py`の中で，ツイートを通知したくないアカウント(`BLOCK_LIST`)を設定することができます．
    * デフォルトではいくつかの翻訳botを追加しております．

    ```python
    BLOCK_LIST = set(
        [
            "arXiv_cs_CV_ja",
            "arXiv_cs_CL_ja",
            "hackernewsj",
        ]
    )
    ```

1. (任意) ツイートを取得したいユーザーの設定
    * `src/setting.py`の中にツイートを取得したいユーザー(`USERS`)を設定できます．
    * デフォルトでは論文に関するツイートを多くしてくれるAKさん(@ak92501)からのツイートを取得するようになってます．

    ```python
    USERS = [
        "ak92501",
    ]
    ```
    
1. (任意) 通知の日時の設定
    * `.github/workflows/notify.yml`の中の`cron`の値を変更することで，通知の日時を変更できます．
    * デフォルトでは日本時間の朝9時に通知されるようになっています．

    ```yaml
    name: paper-summary-tweet-notification

    on:
      schedule:
        # 通知時間を変更したい場合は，以下を変更する
        # UTC 0時 -> 日本時間朝9時
        - cron:  '0 0 * * *'
      workflow_dispatch:

    ...
    ```

## TODO

* [ ] arXiv論文のカテゴリを使用して，興味のある分野の論文に関するツイートのみを通知する
* [ ] 機械学習関連のGitHubレポジトリを引用しているツイートの取得
* [ ] いいねやリツイート数での優先度付け
* [ ] 取得漏れの原因調査
* [ ] `USERS`に設定したユーザーのツイートは，全段のクエリ検索によるツイートの取得部分で通知しないようにする

## Reference

* [論文の日本語要約ツイートをslack / LINEに通知するアプリを作った - yiskw note](https://yiskw713.hatenablog.com/entry/2021/11/10/223848)
