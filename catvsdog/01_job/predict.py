import os
import utils
import config
import traceback
import argparse
from luna import LunaExcepion

from keras.models import load_model


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='1', help='1: small cnn. 2: top trained. 3: fine tuned')
    parser.add_argument('--image', required=True, help='input an image to predict')
    return parser.parse_args()


if __name__ == '__main__':
    try:
        utils.lock()

        args = parse_args()
        if not os.path.exists(args.image):
            raise LunaExcepion(config.inputerr)

        if args.model == '1':
            # 学習済みのモデルをロード
            model = load_model(os.path.join(config.result_dir, 'scratch_model.h5'))
            model.summary()
            # 画像を読み込んで4次元テンソルへ変換
            img = image.load_img(args.image, target_size=(config.img_height, config.img_width))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            # 学習時にImageDataGeneratorのrescaleで正規化したので同じ処理が必要
            x = x / 255.0
            # クラスを予測
            # 入力は1枚の画像なので[0]のみ
            pred = model.predict(x)[0]

            # {'dog': 1, 'cat': 0}
            print(pred)
        elif args.model == '2':
            print(args.model)
        elif args.model == '3':
            print(args.model)
        else:
            raise LunaExcepion(config.inputerr)
    except (KeyboardInterrupt, SystemExit):
        utils.unlock()
        utils.error(config.syserr)
    except LunaExcepion as e:
        utils.error(e.value)
    except Exception as e:
        utils.error(config.syserr)
        print(e)
        print(traceback.format_exc())
    utils.unlock()
