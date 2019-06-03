import random
import solver
from PIL import Image

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line


# Painting Board Subwidget:
# Define a widget and the corresponding UI operations for painting
# 画板子组件：
# 为了实现画图，定义了一个Widget组件以及相关的UI动作
class PaintWidget(Widget):
    color = (254, 0, 0, 1)  # Pen color  画笔颜色
    thick = 8  # Pen thickness  画笔粗度

    def __init__(self, root, **kwargs):
        super().__init__(**kwargs)
        self.parent_widget = root

    # Touch down motion:
    # If the touch position is located in the painting board, draw lines.
    # 按下动作：
    # 如果触摸位置在画板内，则在画板上划线
    def on_touch_down(self, touch):
        with self.canvas:
            Color(*self.color, mode='rgba')
            if touch.x > self.width or touch.y < self.parent_widget.height - self.height:
                return
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=self.thick)

    # Touch move motion:
    # Draw line with mouse/hand moving
    # 移动动作：
    # 随着鼠标/手指的移动画线
    def on_touch_move(self, touch):
        with self.canvas:
            if touch.x > self.width or touch.y < self.parent_widget.height - self.height:
                return
            touch.ud['line'].points += [touch.x, touch.y]

    # Touch up motion:
    # When ending drawing line, save the picture, and call the prediction component to do prediction
    # 抬起动作：
    # 结束画线，保存图片成文件，并调用预测相关的组件做预测
    def on_touch_up(self, touch):
        if touch.x > self.width or touch.y < self.parent_widget.height - self.height:
            return
        #self.parent.parent.do_predictions()

    def export_image(self):
        input_img_name = './input_expression.png'
        self.export_to_png(input_img_name)
        im = Image.open(input_img_name)
        x, y = im.size
        p = Image.new('RGBA', im.size, (255, 255, 255))
        p.paste(im, (0, 0, x, y), im)
        p.save('white_bg.png')

        return 'white_bg.png'


# Recognizer
# Define the application window, and some corresponding operations
# 识别器
# 定义程序窗口，并实现一些操作逻辑
class Recognizer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.number = -1  # Variable to store the predicted number  保存识别的数字的变量
        self.orientation = 'horizontal'  # UI related  UI相关
        self.draw_window()

    # function to declare the components of the application, and add them to the window
    # 声明程序UI组件的函数，并且将它们添加到窗口上
    def draw_window(self):
        # Clear button  清除按钮
        self.clear_button = Button(text='CLEAR', font_name=HandwrittenMathCalculator.font_name, size_hint=(1, 4 / 45),
                                   background_color=(255, 165 / 255, 0, 1))
        self.solve_button = Button(text='SOLVE', font_name=HandwrittenMathCalculator.font_name, size_hint=(1, 4 / 45),
                                   background_color=(255, 165 / 255, 0, 1))
        # Painting board  画板
        self.painter = PaintWidget(self, size_hint=(1, 8 / 9))
        # Label for hint text  提示文字标签
        self.hint_label = Label(font_name=HandwrittenMathCalculator.font_name, size_hint=(1, 1 / 45))
        # Label for predicted number  识别数字展示标签
        self.result_label = Label(font_size=120, size_hint=(1, 1 / 3))
        # Label for some info  展示一些信息的标签
        self.info_board = Label(font_size=24, size_hint=(1, 22 / 45))

        # BoxLayout  盒子布局
        first_column = BoxLayout(orientation='vertical', size_hint=(2 / 3, 1))
        second_column = BoxLayout(orientation='vertical', size_hint=(1 / 3, 1))
        # Add widgets to the window  将各个组件加到应用窗口上
        first_column.add_widget(self.painter)
        first_column.add_widget(self.hint_label)
        second_column.add_widget(self.result_label)
        second_column.add_widget(self.info_board)
        second_column.add_widget(self.solve_button)
        second_column.add_widget(self.clear_button)
        self.add_widget(first_column)
        self.add_widget(second_column)

        # motion binding  动作绑定
        # Bind the click of the clear button to the clear_paint function
        # 将清除按钮的点击事件绑定到clear_paint函数上
        self.clear_button.bind(on_release=self.clear_paint)
        self.solve_button.bind(on_release=self.solve_expression)

        self.clear_paint()  # Initialize the state of the app  初始化应用状态

        # Clear the painting board and initialize the state of the app.
    def clear_paint(self):
        self.painter.export_image()
        #call solver to solve


    # Clear the painting board and initialize the state of the app.
    def clear_paint(self, obj=None):
        self.painter.canvas.clear()
        self.number = -1
        self.result_label.text = '?'
        self.hint_label.text = 'Write math expression above'
        self.info_board.text = 'Detected expression:\n'

    # Extract info from the predictions, and display them on the window
    # 从预测结果中提取信息，并展示在窗口上
    def show_info(self, result, detected_expression='8+7'):
        if result == None:
            self.number = 'Error'
        else:
            self.number = result
        self.result_label.text = str(self.number)
        self.hint_label.text = 'Detected expression and result is shown.Press clear to Retry!'
        self.info_board.text += detected_expression

    # Use CNN predictor to do prediction, and call show_info to display the result
    # 使用CNN预测器做预测，并调用show_info函数将结果显示出来
    def solve_expression(self, obj=None):
        img = self.painter.export_image()
        self.info_board.text = 'Detected expression:\n'
        (result,detected_expression) = solver.solve(img)
        self.show_info(result,detected_expression)



# Main app class
# 主程序类
class HandwrittenMathCalculator(App):
    font_name = r'Arial.ttf'
    def build(self):
        return Recognizer()


if __name__ == '__main__':
    HandwrittenMathCalculator().run()
