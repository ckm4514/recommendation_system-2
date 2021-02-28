import numpy as np
import keras
from sklearn.utils import shuffle

from NeuMF import NeuMF
from Data_latest import Data
from get_log import get_log
from train_model import train_model
from args import Args


def main(args, logger, train_dataset):

    # Instantiate an optimizer.
    optimizer = keras.optimizers.Adam(learning_rate=args['LR'])
    # Instantiate a loss function.
    criterion = keras.losses.BinaryCrossentropy(from_logits=True)

#===============================================
    loader = Loader()

    print('start data load..')

    uids, iids, df_train, df_test, \
    df_neg, users, items, item_lookup = loader.load_dataset()
    user_input, item_input, labels = loader.get_train_instances(uids, iids, args['NUM_NEG'], len(items))

    print('end data load..')

    # input data 준비
    user_data_shuff, item_data_shuff, label_data_shuff = shuffle(user_input, item_input, labels)
    user_data_shuff = np.array(user_data_shuff).reshape(-1, 1)
    item_data_shuff = np.array(item_data_shuff).reshape(-1, 1)
    label_data_shuff = np.array(label_data_shuff).reshape(-1, 1)
# ===============================================

    # collab_mapped.csv 있어야함
    data = Data()
    df_order = data.load_df()
    uid, iid, df_train, df_test, user, item, df_neg = data.prepaer_df(df_order)
    user_input, item_input, label = data.get_train_instances(uid, iid, len(item))

    # Model initialize
    model = NeuMF(user_input, item_input)
    train_model(model, train_dataset, valid_dataset, criterion, optimizer, args, logger)


if __name__ == "__main__":
    args = Args().params
    logger = get_log()
    main(args, logger, train_dataset)