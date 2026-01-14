import re
import time
import cv2

def ensure_cv2_windows_closed():
    try:
        cv2.destroyAllWindows()
    except:
        pass

from qfluentwidgets import FluentIcon

from src.tasks.MyBaseTask import MyBaseTask

class MyOneTimeTask(MyBaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "每日炒货当倒勾"
        self.description = "识别并买卖当天最赚钱的产品，请确保调度券充足"
        self.icon = FluentIcon.SYNC
        self.default_config.update({
            '下拉菜单选项': "第一",
            '是否选项默认支持': False,
            'int选项': 1,
            '文字框选项': "默认文字",
            '长文字框选项': "默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字默认文字",
            'list选项': ['第一', '第二', '第3'],
        })
        self.config_type["下拉菜单选项"] = {'type': "drop_down",
                                      'options': ['第一', '第二', '第3']}

    def run(self):
        """主运行方法"""
        self.log_info('每日炒货任务开始运行!', notify=True)

        # 第一步：检测坐标范围
        self.check_and_handle_start_screen()

        self.log_info('每日炒货任务运行完成!', notify=True)

    def check_and_handle_start_screen(self):
        # 确保所有cv2窗口都已关闭，避免影响find_one
        ensure_cv2_windows_closed()
        # 同时检测两个指定的图片
        is_friend_home = self.find_one('in_friend_home_or_not')
        is_in_domain = self.find_one('in_domain_or_not')
        # 如果检测到任意一个目标图片，按Esc键
        if is_friend_home or is_in_domain:
            self.do_send_key_down('esc')
            self.do_send_key_up('esc')
            # 按ESC后持续识别have_tech_or_not图片并按T
            self.wait_and_press_t_when_tech_found()
            # 根据检测到的图片类型记录要等待的退出图片
            target_leave_image = None
            if is_friend_home:
                self.log_info("检测到目标图片（in_friend_home_or_not），已按Esc键")
                target_leave_image = 'leave_friend_home'
            elif is_in_domain:
                self.log_info("检测到 in_domain_or_not 图片，已按Esc键")
                target_leave_image = 'leave_domain'
            # 等待对应的退出图片出现并点击
            if target_leave_image:
                self.wait_and_click_leave_image(target_leave_image)
        else:
            # 如果两个都没有检测到，按M键
            self.do_send_key_down('m')
            self.do_send_key_up('m')
            self.log_info("未检测到目标图片，已按M键")
            # 按M键后检测是否在地图中
            self.check_in_map_and_press_esc()

    def wait_and_click_leave_image(self, target_leave_image):
        self.log_info(f"开始等待退出图片: {target_leave_image}")

        # 设置超时时间
        timeout = 10
        start_time = time.time()
        while time.time() - start_time < timeout:
            # 确保所有cv2窗口都已关闭，避免影响find_one
            ensure_cv2_windows_closed()
            # 检测指定区域是否出现退出图片
            leave_image_pos = self.find_one(target_leave_image)

            # 打印find_one的结果
            self.log_info(f"find_one('{target_leave_image}') 返回结果: {leave_image_pos}")

            if leave_image_pos:
                # 获取图片位置并点击
                self.log_info(f"检测到退出图片 {target_leave_image}")
                self.click_box(leave_image_pos)
                self.log_info(f"已点击退出图片: {target_leave_image}")
                # 点击退出图片后按M键并检测是否在地图中
                self.log_info("点击退出图片后按M键")
                self.do_send_key_down('m')
                self.do_send_key_up('m')
                self.check_in_map_and_press_esc()
                return True
        # 超时处理
        self.log_info(f"等待退出图片 {target_leave_image} 超时")
        return False

    def wait_for_start_images_gone_and_press_m(self):
        self.log_info("确认是否已完全退出...")

        # 设置超时时间（可以根据实际情况调整）
        timeout = 10
        start_time = time.time()
        while time.time() - start_time < timeout:
            # 确保所有cv2窗口都已关闭，避免影响find_one
            ensure_cv2_windows_closed()
            # 同时检测两个指定的图片
            is_friend_home = self.find_one('in_friend_home_or_not')
            is_in_domain = self.find_one('in_domain_or_not')
            # 如果两个图片都不存在，按M键并返回
            if not is_friend_home and not is_in_domain:
                self.do_send_key_down('m')
                self.do_send_key_up('m')
                self.log_info("确认已完全退出，已按M键")
                # 按M键后检测是否在地图中
                self.check_in_map_and_press_esc()
                return True
        # 超时处理
        self.log_info("等待退出确认超时")
        return False
    
    def check_in_map_and_press_esc(self):
        """检测是否在地图中，如果是则按ESC键"""
        # 确保所有cv2窗口都已关闭，避免影响find_one
        ensure_cv2_windows_closed()
        # 检测是否存在in_map_or_not图片
        is_in_map = self.find_one('in_map_or_not')
        if is_in_map:
            self.log_info("检测到in_map_or_not图片，已按ESC键")
            self.do_send_key_down('esc')
            self.do_send_key_up('esc')
            # 按ESC后持续识别have_tech_or_not图片并按T
            self.wait_and_press_t_when_tech_found()
            return True
        else:
            self.log_info("未检测到in_map_or_not图片")
            return False
    
    def wait_and_press_t_when_tech_found(self):
        """持续识别图片have_tech_or_not，识别到后按T"""
        self.log_info("开始持续识别have_tech_or_not图片...")
        
        # 设置超时时间（可以根据实际情况调整）
        timeout = 30
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # 确保所有cv2窗口都已关闭，避免影响find_one
            ensure_cv2_windows_closed()
            # 检测是否存在have_tech_or_not图片
            have_tech = self.find_one('have_tech_or_not')
            
            if have_tech:
                self.log_info("检测到have_tech_or_not图片，已按T键")
                self.do_send_key_down('t')
                self.do_send_key_up('t')
                return True
            
            # 短暂延迟后继续检测
            time.sleep(0.5)
        
        # 超时处理
        self.log_info("等待识别have_tech_or_not图片超时")
        return False






    def find_some_text_on_bottom_right(self):
        return self.ocr(box="bottom_right",match="商城", log=True) #指定box以提高ocr速度

    def find_some_text_with_relative_box(self):
        return self.ocr(0.5, 0.5, 1, 1, match=re.compile("招"), log=True) #指定box以提高ocr速度

    def test_find_one_feature(self):
        return self.find_one('box_battle_1')

    def test_find_feature_list(self):
        return self.find_feature('box_battle_1')

    def run_for_5(self):
        self.operate(lambda: self.do_run_for_5())

    def do_run_for_5(self):
        self.do_send_key_down('w')
        self.sleep(0.1)
        self.do_mouse_down(key='right')
        self.sleep(0.1)
        self.do_mouse_up(key='right')
        self.sleep(5)
        self.do_send_key_up('w')
