import logging
from airtest.core.api import *
from cv2 import threshold
from threading import Thread
from lib.iphone15promax import iphone15promax as iphone


logger = logging.getLogger("actions")
logger.setLevel(logging.INFO)
print(logger.handlers)
# logger.handlers[0].setFormatter(
#     logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s'))


class op:
    """
    各种点击操作
    """
    def attack(x: int, y: int, x2: int, y2: int, x3: int, y3: int, delay=20):
        """
        开始攻击，传入三张卡的位置和宝具时间，默认20s
        (x,y)取值: (1,1)-(1,3)，(2,1)-(2,5)
        第一行宝具卡，第二行普通指令卡
        """
        logger.debug("攻击")
        # touch(iphone.attackBtn)
        touch(Template(r"common/攻击.jpeg", threshold=0.8,
                       rgb=True))
        sleep(1)
        touch(iphone.attackPos[x - 1][y - 1])
        sleep(1)
        touch(iphone.attackPos[x2 - 1][y2 - 1])
        sleep(1)
        touch(iphone.attackPos[x3 - 1][y3 - 1])
        sleep(delay)
        touch([10, 300])
        sleep(5)

    def finalAttack(timeout=10):
        """
        看情况补个刀，队伍不稳定时用。稳定时别用，拖速度
        """
        try:
            wait(Template(r"common/攻击.jpeg", threshold=0.8,
                 rgb=True), timeout=timeout, interval=1)
            logger.debug("补刀")
            op.attack(2, 1, 2, 4, 2, 5, 0)
            sleep(5)
            touch([10, 300])
            sleep(5)
        except TargetNotFoundError:
            pass

    def chooseFriend(friend):
        """
        助战选择，传入图片文件路径，或一个屏幕坐标，比如[1121,332]
        """
        if not isinstance(friend, str):  # if not string,treate it as coordiante
            touch(friend)
            sleep(1)
        else:
            swipe_count = 7
            while True:
                coor = exists(Template(friend, threshold=0.8, rgb=True))
                if not coor:
                    swipe([500, 900], [500, 500])
                    swipe_count -= 1
                else:  # Choose friend and break
                    touch(coor)
                    sleep(2.2)
                    break
                if swipe_count == 0:
                    touch(iphone.refreshList)  # 列表刷新
                    sleep(1)
                    touch(iphone.refreshBtn)  # 是
                    sleep(1)
                    swipe_count = 5
            if swipe_count == -1:
                return  # TODO 错误处理
        coor = exists(Template(r"common/开始任务.png", threshold=0.8))
        if coor:
            touch(coor)
        sleep(3)

    def skillChoose(servant: int, skill: int, svt=-1, delay=1.2):
        """
        选择从者技能
        servant: 从者位置，取值1-3
        skill: 技能位置, 取值1-3
        svt: （可选）单体技能给别人的位置，取值 1-3
        """
        sleep(1)
        touch(iphone.skillChoose[servant - 1][skill - 1])
        if svt != -1:
            sleep(1)
            touch(iphone.skillSvtPos[svt - 1])
        touch(iphone.nextBtn)
        sleep(delay)

    def masterSkillChoose(num: int, svt=-1, delay=1.3):
        """
        选择 master 的技能,
        num: 御主技能位置，取值 1-3
        svt: （可选）单体技能给别人的位置，取值 1-3
        """
        touch(iphone.masterSkill)
        sleep(1)
        touch(iphone.masterSkillPos[num - 1])
        # touch(iphone.skillConfirmBtn)
        sleep(1)
        if svt != -1:
            touch(iphone.skillSvtPos[svt - 1])
            touch([10, 300])
        sleep(delay)

    def masterChangeOrderPos(svt1: int, svt2: int, delay=2):
        """
        换人服的从者位置，svt1, svt2 为从者位置，取值 1-6，且不可为相同数字
        """
        touch(iphone.orderPos[svt1 - 1])
        sleep(1)
        touch(iphone.orderPos[svt2 - 1])
        sleep(1)
        touch(iphone.orderPosConfirm)  # 进行更替
        sleep(delay)

    def ending(eatApple):
        wait(
            Template(  # 现在改名叫牵绊了，反正能用，将就了
                r"common/与从者的羁绊.png", record_pos=(-0.351, -0.136), resolution=(2208, 1242)
            ),
            timeout=45,
            interval=2,
        )
        touch(iphone.nextBtn)
        sleep(1)
        touch(iphone.nextBtn)
        sleep(1)
        touch(iphone.nextBtn)
        sleep(1)  # 防止意外情况，升级什么的
        touch(iphone.nextBtn)
        sleep(1)
        touch(iphone.closeFrd)
        sleep(.5)
        touch(iphone.continueBattleBtn)
        sleep(1)
        logger.debug("吃苹果 %s" % str(eatApple))
        if eatApple:
            op._eatApple()
        sleep(3)
        logger.debug("结尾动画处理完毕")

    def _eatApple():
        """
        检测是否出现苹果补充界面，出现了就补苹果
        """
        coor = exists(Template(r"common/白银果实.jpeg", threshold=0.7, rgb=True))
        if not coor:
            coor = exists(Template(r"common/黄金果实.jpeg",
                          threshold=0.7, rgb=True))
        if coor:
            touch(coor)
            sleep(.5)
            touch(iphone.confirmApple)
            sleep(1.3)
        else:
            logger.debug("无苹果页")

    def clickRetry():
        coor = exists(Template(r"common/重试.jpeg"))
        if coor:
            touch(coor)


def unlimited():
    """
    抽无限池
    """
    while 1:
        touch(iphone.unlimitedReset, 200)
