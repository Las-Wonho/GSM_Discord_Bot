from WebCrawler import WebCrawler

from datetime import datetime
import random

class WebManager:
    def get_nextDay(self):
        today = datetime.today()
        nextMeal = self.get_nextMeal(today) # 아침, 점심, 저녁, 다음 날 아침중에 어떤 식사를 불러와야 하는지를 나타내는 정수

        try:
            today = today.replace(day = today.day + int(nextMeal / 3)) # 다음 날 아침을 불러와야 한다면 today에 다음 날로 바꾼 datetime 객체를 넣음
        except ValueError: # 한 달의 마지막 날에서 1이 더해진다면 ValueError가 발생하므로 예외 처리
            try:
                today = today.replace(month = today.month + 1, day = 1) # 다음 달 1일로 바꾼 datetime 객체를 넣어준다
            except ValueError: # 한 해의 마지막 달에서 1이 더해진다면 ValueError가 발생하므로 예외 처리
                today = today.replace(year = today.year + 1, month = 1, day = 1) # 다음 년도 1월 1일로 바꾼 datetime 객체를 넣어준다
                
        return today

    def get_nextMeal(self, today):
        time = [480, 810, 1170] # 각각 아침, 점심, 저녁을 먹는 시간(분 단위로 환산함)
        
        for i in range(len(time)):
            if (today.hour * 60 + today.minute) < time[i]:
                return i
        return len(time)

    def get_info(self, command, keyword = None):
        return getattr(self, "get_%s" % command, "%s 작업을 처리하는데 문제가 발생했습니다." % command)(keyword)

    def get_hungry(self, dump):
        today = self.get_nextDay()
        nextMeal = self.get_nextMeal(today)
        item = ["아침", "점심", "저녁"]

        soup = WebCrawler().get_soup("http://www.gsm.hs.kr/xboard/board.php?tbnum=8")

        try:
            info = soup.select("#xb_fm_list > div.calendar > ul > li > div > div.slider_food_list.slider_food%s.cycle-slideshow" % today.day)
            menuList = (info[0].find("div", {"data-cycle-pager-template" : "<a href=#none; class=today_food_on%s title=%s></a>" % (nextMeal % 3 + 1, item[nextMeal % 3])}).find("span", "content").text).split("\n")

            for i in range(2): # 탄수화물, 단백질 등의 표시를 제외하고 출력하기 위해 맨 끝에 두 개를 지움
                del menuList[-1]

            result = ""
            for i in menuList:
                result +=  ("- "+ i.split()[0] + "\n")
            return result

        except:
            print("[오류] GSM Bot이 식단표를 받아올 수 없습니다.")
            return "%s 급식을 불러올 수 없습니다." % item[nextMeal]

    def get_calendar(self, dump):
        today = datetime.today()

        soup = WebCrawler().get_soup("http://www.gsm.hs.kr/xboard/board.php?tbnum=4")

        try:
            info = soup.select("#xb_fm_list > div.calendar > ul > li > dl")
            
            result = "```"
            for i in info:
                if not i.find("dd") == None:
                    text = i.text.replace("\n", "")
                    result += "%6s -%s\n" % (text.split("-")[0], text.split("-")[1])
            result += "```"
            return result

        except AttributeError:
            print("[오류] GSM Bot이 학사일정을 불러올 수 없습니다.")
            return "%s년 %s월 학사일정을 불러올 수 없습니다." % (today.year, today.month)

    def get_image(self, keyword):
        soup = WebCrawler().get_soup("https://www.google.co.kr/search?tbm=isch&q=%s" % keyword)

        try:
            info = soup.find_all("img")
            index = random.randint(1, len(info)) # 구글 자체 이미지가 포함되어 있기 때문에 1부터 시작한다
            return info[index]["src"] # 이미지의 링크를 가져옴

        except:
            print("[오류] GSM Bot이 이미지를 가져올 수 없습니다.")
            return None

if __name__ == "__main__":
    pass
