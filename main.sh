#! /bin/bash
SHELL_DIR=${0%/*}
## shellのパラメーター
# 購入対象ITEMURL
export START_URL=$1
# 購入するなら1、しないならそれ以外
export PURCHASE_FLG=$2

export EMAIL="XXXXXX"
export PASSWORD="XXXXXX"

export PIC_DIR="${SHELL_DIR}/picture"
export LOG_DIR="${SHELL_DIR}/log"
export TMP_DIR="${SHELL_DIR}/tmp"
#export DATE=`date "+%Y%m%d_%H%M%S"`
export PHANTOM_PATH=`which phantomjs`
export FIREFOX_PROFILE=`ls -d /home/$USER/.mozilla/firefox/*.default/`

# NULL判定
export DATE=`date '+%Y%m%d'`
export LOCK_FILE="purchase_${DATE}.lock"
export END_FILE="purchase_${DATE}.end"
echo $LOCK_FILE
# 
# ディレクトリがなければ作成
mkdir -p $LOG_DIR 2>/dev/null
mkdir -p $PIC_DIR 2>/dev/null
mkdir -p $TMP_DIR 2>/dev/null

# ロックファイルの作成
if [ ! -e $TMP_DIR/$LOCK_FILE ]; then   
    touch $TMP_DIR/$LOCK_FILE
fi

# 購入プログラム実行
python ${SHELL_DIR}/pom_purchase_shot.py > "$LOG_DIR/main_${DATE}.log"

