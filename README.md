# CLANNAD Face Detection

日本語の説明：https://github.com/rtorii/CLANNAD-Face-Detection/blob/main/README_ja.md

**Description：**

A program that detects the face(s) of character(s) from the anime CLANNAD and outputs the name of the character(s) and their location in the image. The reason I choose CLANNAD for face detection is because the characters from CLANNAD have similar eye shape and I thought it is difficult to correctly detect each character compared to charcters in other animes.  The program can detect 8 characters mentioned in CLANNAD's [official homepage](https://www.tbs.co.jp/clannad/clannad1/04chara/chara.html).

  | Input image | Output image |
  | ------ | ------ |
  | ![くらなど](https://user-images.githubusercontent.com/52717342/175796835-4bb0178b-7631-4cb9-b43f-c0a9670c3118.jpeg) | ![f2c533a00ecb95ead668ed36a7c42963b3d02ce64691bf10c2b779dd](https://user-images.githubusercontent.com/52717342/175796837-a6d859ba-1072-410f-a5b4-cf936ebfec58.jpeg) |
  | © VisualArt's/Key/光坂高校演劇部 ／Source: [RENOTE](https://renote.jp/articles/11191) |  |




**Files：**

- ```lbpcascade_animeface.xml``` - [Cascade file](https://github.com/nagadomi/lbpcascade_animeface) used to detect anime faces.
- ```face.py``` - Uses ```lbpcascade_animeface.xml``` to detect faces from images and save the facial images.
- ```da.py``` - Used to increase the amount of train data by creating images of different blur levels and brightness. 
- ```train.py``` - Creates the model and tests it on test data.
- ```model_200_160_80_epoch30_30.h5``` - Model to detect CLANNAD character from facial images.
- ```test.py``` - Takes in an image and outputs the name of the character(s) and their location in the image.
- ```app.py``` - Uses Streamlit to make a web app.
  - Link to the web app: https://rtorii-clannad-face-detection-app-6furpy.streamlitapp.com/


# What I did step by step

    1. Data (facial images of each character) collection and classification.
    2. Increase the amount of train data (data augmentation).
    3. Create a model.
    4. Test the model. 
    5. Create a program to take in an image and output the name of the character(s) and their location in the image.
    6. Use Streamlit to convert the program into a web app.

1 .  **Data (facial images of each character) collection and classification.```face.py```**
- Collected images from CLANNAD by taking screenshots on episodes (from episode 1 to episode 22). Used ``lbpcascade_animeface.xml``` to detect faces from the screenshots and saved the facial images. 
- Classified all facial images manually, and saved the images with the same character in the same folder.
- Used Python library, ```split-folder```, to divide the images into train set and test set.

    |  Character  |  # of images collected（train set : test set）   |  Character   |# of images collected（train set : test set）    |
    | --- | --- | --- | --- | 
    |   Fuko Ibuki  |   133 (106 : 27)  |  Kotomi Ichinose  | 127 (101 : 26)   |
    |   Kyou Fujibayashi  |   96 (76 : 20)  |   Nagisa Furukawa  |  229 (184 : 45)   |
    |   Ryou Fujibayashi  |  88 (70 : 18)   |  Tomoya Okazaki   |  286 (231 : 55)   | 
    |   Tomoyo Sakagami |  128 (102 : 26)  |  Youhei Sunohara   |  119 (95 : 24)  |

    ※ Although Youhei Sunohara has scenes in CLANNAD ～After Story～ where he has dark hair, I used images of him in blonde hair in this project since his hair is blonde in CLANNAD (from episode 1 to episode 22).

2 . **Increase the amount of train data (data augmentation).　```da.py```**
- For each image in the train set, the program created 3 images with different blur levels. In addition, it created 5 images with different brightness after creating 3 images with different blur levels. The number of images in the train set is increased by 3 x 5 = 15 times its original.
- The total number of training images for the eight characters became 14,475.

    |  Character   |  # of training images    |  Character   | # of training images     |
    | --- | --- | --- | --- | 
    |   Fuko Ibuki  |   1590  |  Kotomi Ichinose   | 1515    |
    |   Kyou Fujibayashi  |   1140  |   Nagisa Furukawa  |  2760   |
    |   Ryou Fujibayashi  |  1050   |  Tomoya Okazaki   |  3465   | 
    |   Tomoyo Sakagami  |  1530   |  Youhei Sunohara   |  1425   |


3 . **Create a model. ```train.py```**
- KerasでSequentialモデル（4層のニューラルネットワーク）を作成します。そして100x100のサイズにリサイズした訓練用画像全てに対して学習させます。リサイズした理由は、```lbpcascade_animeface.xml```で切り取られた画像は正方形ですが、サイズが同じとは限らないためです。
- モデルはそれぞれのマスのRGB情報（100x100x3 = 30000）を入力として受け入れ、8つの出力層（8人のキャラクターを認識するため）があります。一番出力値が高いキャラクターを画像のキャラクターとして認識します。
- エポック数を30（過学習しない程度）に設定しました。

    ```
    Epoch 21/30
    483/483 [==============================] - 6s 12ms/step - loss: 0.1139 - accuracy: 0.9727
    Epoch 22/30
    483/483 [==============================] - 6s 12ms/step - loss: 0.1058 - accuracy: 0.9719
    Epoch 23/30
    483/483 [==============================] - 7s 14ms/step - loss: 0.0948 - accuracy: 0.9771
    Epoch 24/30
    483/483 [==============================] - 7s 14ms/step - loss: 0.0843 - accuracy: 0.9800
    Epoch 25/30
    483/483 [==============================] - 6s 13ms/step - loss: 0.0765 - accuracy: 0.9825
    Epoch 26/30
    483/483 [==============================] - 6s 12ms/step - loss: 0.0761 - accuracy: 0.9813
    Epoch 27/30
    483/483 [==============================] - 6s 12ms/step - loss: 0.0686 - accuracy: 0.9844
    Epoch 28/30
    483/483 [==============================] - 6s 12ms/step - loss: 0.0636 - accuracy: 0.9843
    Epoch 29/30
    483/483 [==============================] - 6s 13ms/step - loss: 0.0574 - accuracy: 0.9869
    Epoch 30/30
    483/483 [==============================] - 6s 13ms/step - loss: 0.0513 - accuracy: 0.9882
    ```
4 . **Test the model. ```train.py```**
- モデルをテスト用画像でテストした結果、全体の正解率は226 / 241 = 93.8%でした。
- 岡崎朋也は、訓練用画像の枚数が一番多かったためか、全てのテスト用画像で正確に認識しました。
- 姉妹の藤林杏と藤林涼が同じ髪色で、訓練用画像の枚数が他のキャラクターと比べ少なかったこともあってか、正解率が他のキャラクターより低い結果となりました。


  |  キャラクター   |   正解数  |  テスト用画像の枚数   | 正解率   | キャラクター   |  正解数   |  テスト用画像の枚数   | 正解率   |
  | --- | --- | --- | --- | --- | --- | --- | --- | 
  |   伊吹風子  |  26   |   27  |  96.3%   |  一ノ瀬ことみ   |  24   | 26   |  92.3%  | 
  |  藤林杏   |   17  |  20   |   85%  |  古川渚   |  43   |  45   |  95.6%   | 
  |  藤林涼   |  15   |   18  |   83.3%  |   岡崎朋也  |  55   |  55   |   100%    | 
  |  坂上智代   |  23   |  26   |  88.5%  |  春原陽平   |  23   |  24   |  95.8%   | 

5 . **Create a program to take in an image and output the name of the character(s) and their location in the image.```test.py```**

  アニメの画像（出典元が加工を許可していないもの）を加工し、インターネットに掲載することは著作権を侵害するという記事を見たので、今回は、白色の背景にキャラクターの名前と位置を示す画像を出力しました。  

**プログラムの手順：**
1. ```lbpcascade_animeface.xml```を使用し、画像から顔を認識する。
2. 認識した顔それぞれをモデルに入力し、出力の中で最も値が高いキャラクターを画像のキャラクターとして認識する。
3. 認識したキャラクターの名前と位置を示す画像を出力する。

  | 入力画像 | 出力画像 |
  | ------ | ------ |
  | ![5aca841a5e7f9cb1fa2fe36d74f51c486e17d7d2d0715424effb70ab](https://user-images.githubusercontent.com/52717342/175799918-d6354880-c3ba-4f1b-829c-94e07b80b43e.jpeg) | ![f45514849387e57cca1283ba6311a07841285ef809d10fd42e28842f](https://user-images.githubusercontent.com/52717342/175799923-161d704f-fdc0-4945-ad04-cc6cd7823cb7.jpeg) |
  | © VisualArt's/Key/光坂高校演劇部 ／引用元: [アニメミル](https://animemiru.jp/articles/7675/) |  |

- 目をつぶっている古川渚と泣いている春原陽平を認識できました。坂上智代は横顔のため、```lbpcascade_animeface.xml```は顔として認識しません。

| 入力画像 | 出力画像 |
| ------ | ------ |
| ![25a02d32019f1987c8fa9a83b159cfa6b891afbe2346d2d3122d07b10cc1766f _SX1080_](https://user-images.githubusercontent.com/52717342/175796378-d3f18259-b42b-45ee-ae19-a43b3e3724a6.jpg) | ![696b9da8dc6eac7d29d7a1c5d4db7dd0f19f2c69e7944f40a04813ec](https://user-images.githubusercontent.com/52717342/175796921-2646e6b2-0125-444b-9e34-ff99aa62e089.jpeg) |
| © VisualArt's/Key/光坂高校演劇部 ／引用元: [Amazon](https://www.amazon.co.jp/CLANNAD-AFTER-STORY%E3%80%90TBS%E3%82%AA%E3%83%B3%E3%83%87%E3%83%9E%E3%83%B3%E3%83%89%E3%80%91/dp/B00FYKXTGS) |  |

- 姉妹の藤林涼と藤林杏を認識。

| 入力画像 | 出力画像 |
| ------ | ------ |
| ![t02200154_0342024012866838688](https://user-images.githubusercontent.com/52717342/175796415-5c420ac1-446b-4d48-89a6-528d5ed6f1c9.jpeg) | ![5c3ed7ae87c874586f77c27bedb77fd96842877d04f4996b4f4db944](https://user-images.githubusercontent.com/52717342/175796419-63f97fc3-b029-4b31-85af-dd06d8694dc9.jpeg) |
| © VisualArt's/Key/光坂高校演劇部 ／引用元: [ameblo](https://ameblo.jp/i-was-me/entry-11786945737.html) |  |

- 認識を間違えたケース: 坂上智代を藤林涼と認識。

| 入力画像 | 出力画像 |
| ------ | ------ |
| ![Bz1tgcTCcAACHuH](https://user-images.githubusercontent.com/52717342/175796900-08142f4f-2b32-4bb4-835d-35b1c8686891.jpeg) | ![f8db8d5e20a944cf27be85d13ea744fd469e7283e88fd5c957ba4421](https://user-images.githubusercontent.com/52717342/175796899-7eb7d6d6-e4d3-47ca-86ad-f2b06861c429.jpeg) |
| © VisualArt's/Key/光坂高校演劇部 ／引用元: [Twitter](https://twitter.com/clannadjudo0327/status/521693560672772097/photo/1) |  |

6 . **Use Streamlit to convert the program into a web app.**
- Webアプリのリンク: https://rtorii-clannad-face-detection-app-6furpy.streamlitapp.com/

**Webアプリの使用方法:**
1.  CLANNADのキャラクターの顔が写っている画像をアップロードします。
2.  ```Process```ボタンを押すと出力画像が表示されます。

| ホームページ | 
| ------ |
| <img width="1439" alt="Screen Shot 2022-06-26 at 13 20 10" src="https://user-images.githubusercontent.com/52717342/175799260-cb8ab7e3-ba52-4e46-919c-396fdcfbf745.png"> |

| 出力 | 
| ------ |
| <img width="1439" alt="Screen Shot 2022-06-25 at 23 15 54" src="https://user-images.githubusercontent.com/52717342/175807453-962d14be-2376-4c7b-815c-f9d54187823a.png"> |




Created by Ryota Torii <rtorii@protonmail.com> on 06/26/22
