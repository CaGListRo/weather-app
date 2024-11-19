import requests, sys
import pygame as pg
from icecream import ic
from datetime import datetime

from typing import Final

class WeatherApp:
    WIDTH: Final[int] = 1380 
    HEIGHT: Final[int] = 780
    FPS: Final[int] = 30
    # colors
    BACKGROUND_COLOR: Final[tuple[int]] = (19, 30, 50)
    NORMAL_TEXT_COLOR: Final[tuple[int]] = (247, 247, 247)
    UNDERLINE_COLOR: Final[tuple[int]] = (242, 242, 242)
    RED: Final[tuple[int]] = (255, 0, 0)
    ORANGE: Final[tuple[int]] = (231, 83, 0)
    YELLOW: Final[tuple[int]] = (231, 202, 0)
    SEPARATOR_COLOR: Final[tuple[int]] = (52,42,155)
    ACCENT_COLOR: Final[tuple[int]] = (71, 51, 235)
    SYMBOL_RECT_COLOR: Final[tuple[int]] = (32, 54, 94)
    BUTTON_COLOR: Final[tuple[int]] = (56, 155, 60)
    BUTTON_HOVER_COLOR: Final[tuple[int]] = (76, 175, 80)
    BUTTON_SHADOW_COLOR: Final[tuple[int]] = (36, 135, 40)

    def __init__(self) -> None:
        """ Initializes the weather app. """
        pg.init()

        self.WIN: pg.display = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption("Wetter App Aachen")

        self.clock: pg.time.Clock = pg.time.Clock()

        self.api_adress: str = "https://api.open-meteo.com/v1/forecast?latitude=50.7766&longitude=6.0834&current=temperature_2m,is_day,precipitation,rain,cloud_cover,wind_speed_10m,wind_direction_10m&hourly=precipitation_probability,precipitation,cloud_cover,vapour_pressure_deficit,temperature_180m,uv_index,is_day&daily=temperature_2m_max,temperature_2m_min,daylight_duration,sunshine_duration,uv_index_max,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,wind_direction_10m_dominant&timezone=Europe%2FBerlin&models=best_match,gfs_seamless,jma_seamless,icon_seamless,gem_seamless,meteofrance_seamless"
        # API für Opladen
        # self.api_adress: str = "https://api.open-meteo.com/v1/forecast?latitude=51.0686&longitude=7.0039&current=temperature_2m,is_day,precipitation,rain,cloud_cover,wind_speed_10m,wind_direction_10m&hourly=precipitation_probability,precipitation,cloud_cover,vapour_pressure_deficit,temperature_180m,uv_index,is_day&daily=temperature_2m_max,temperature_2m_min,daylight_duration,sunshine_duration,uv_index_max,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,wind_direction_10m_dominant&timezone=Europe%2FBerlin&models=best_match,gfs_seamless,jma_seamless,icon_seamless,gem_seamless,meteofrance_seamless"
        
        # initialize lists
        self.current_conditions: list[str] = ["cloud_cover", "precipitation", "temperature_2m", "wind_direction_10m", "wind_speed_10m"]
        self.current_weather_texts: list[str] = ["Wolkendecke:", "Niederschlag:", "Temperatur:", "Windrichtung:", "Windstärke:"]
        self.current_weather_units: list[str] = ["%", "mm", "°C", "", "km/h"]
        self.model_list: list[str] = ["best_match", "gem_seamless", "gfs_seamless", "jma_seamless", "icon_seamless", "meteofrance_seamless"]
        self.condition_list: list[str] = ["precipitation_sum", "temperature_2m_max", "temperature_2m_min", "wind_direction_10m_dominant", "wind_speed_10m_max", "daylight_duration", "sunshine_duration", "precipitation_probability_max", "uv_index_max"]
        self.hourly_condition_list: list[str] = ["precipitation_probability", "precipitation", "cloud_cover", "vapour_pressure_deficit", "temperature_180m", "uv_index", "is_day"]
        self.hourly_texts: list[str] = ["Nw:", "Ns:", "Wd:", "Ld:", "Te:", "uv:"]
        self.forecast_texts: list[str] = ["Datum", "Niederschlag:", "Max. Temperatur:", "Min. Temperatur:", "Windrichtung:", "Windstärke:", "Tageslicht:", "Sonnenschein:", "Niederschlagswahrschl.:", "UV-Index:"] 
        self.weather_units: list[str] = ["", "mm", "°C", "°C", "", "km/h", "h", "h", "%", ""]
        self.days_in_german: list[str] = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

        # initialize fonts
        self.HEADING_FONT: pg.font.Font = pg.font.SysFont("comicsans", 23)
        self.MAIN_FONT: pg.font.Font = pg.font.SysFont("comicsans", 17)
        self.HOURLY_FONT: pg.font.Font = pg.font.SysFont("comicsans", 15)
        self.SMALL_FONT: pg.font.Font = pg.font.SysFont("comicsans", 11)

        # initialize colors
        self.refresh_button_color: tuple[int] = self.BUTTON_COLOR
        self.help_button_color: tuple[int] = self.BUTTON_COLOR
        self.back_button_color: tuple[int] = self.BUTTON_COLOR

        # button settings
        self.refresh_button_clicked: bool = False
        self.help_button_clicked: bool = False
        self.back_button_clicked: bool = False
        self.refresh_button_elevation: int = 5
        self.help_button_elevation: int = 5
        self.back_button_elevation: int = 5
        self.refresh_button_rect: pg.Rect = pg.Rect((300, 80), (182,35))
        self.help_button_rect: pg.Rect = pg.Rect((300, 125), (182,35))
        self.refresh_button_shadow: pg.Rect = pg.Rect((300, 80), (182,35))
        self.help_button_shadow: pg.Rect = pg.Rect((300, 125), (182,35))
        self.back_button_rect: pg.Rect = pg.Rect((20, 10), (182,35))
        self.back_button_shadow: pg.Rect = pg.Rect((20, 55), (182,35))

        self.show_help: bool = False
        self.refresh_text_surf: pg.Surface = self.MAIN_FONT.render("Aktualisieren", 1, self.NORMAL_TEXT_COLOR)
        self.refresh_text_rect: pg.Rect = self.refresh_text_surf.get_rect(center=self.refresh_button_rect.center)
        self.help_text_surf: pg.Surface = self.MAIN_FONT.render("?", 1, self.NORMAL_TEXT_COLOR)
        self.help_text_rect: pg.Rect = self.help_text_surf.get_rect(center=self.help_button_rect.center)
        self.back_text_surf: pg.Surface = self.MAIN_FONT.render("Zurück", 1, self.NORMAL_TEXT_COLOR)
        self.back_text_rect: pg.Rect = self.refresh_text_surf.get_rect(center=self.refresh_button_rect.center)

        self.help_file_path: str = "help_text.txt"
        
    def change_date_format(self, date_string: str) -> str:
        """
        Changes the date format from the international format to the German format.
        Args:
        date_string (str): The date string in the international format.
        Returns:
        str: The date string in the German format.
        """
        unformatted_date = datetime.strptime(date_string, "%Y-%m-%d")
        return unformatted_date.strftime("%d.%m.%Y")

    def build_mean(self, best_match_list: list[float], gem_list: list[float], gfs_list: list[float], jma_list: list[float], icon_list: list[float], meteofrance_list: list[float], dates: list[str], daily: bool=True) -> list[float]:
        """
        Builds the mean of the given lists.
        Args:
        best_match_list (list[float]): The list of best match forecasts.
        gem_list (list[float]): The list of GEM forecasts.
        gfs_list (list[float]): The list of GFS forecasts.
        jma_list (list[float]): The list of JMA forecasts.
        icon_list (list[float]): The list of ICON forecasts.
        meteofrance_list (list[float]): The list of MeteoFrance forecasts.
        dates (list[str]): The list of dates.
        daily (bool): Whether to calculate the daily mean or not. Defaults to True.
        Returns:
        list[float]: The mean of the given lists.
        """
        i_range = 9 if daily else 7
        j_range = 7 if daily else 42
        mean_list = []
        
        if daily:
            mean_list.append(dates)
        model_list = [best_match_list, gem_list, gfs_list, jma_list, icon_list, meteofrance_list]

        for i in range(i_range):
            condition_list = []
            for j in range(j_range):
                divider = 6
                sum_var = 0
                for model in model_list:
                    if model[i][j] is not None:
                        sum_var += model[i][j]
                    else:
                        divider -= 1
                mean_var = sum_var / divider if divider != 0 else 0
                condition_list.append(round(mean_var, 1))
            mean_list.append(condition_list)       
        return mean_list

    def get_forecast_list(self, model: str, daily: bool=True) -> list[list[float]]:
        """
        Gets the forecast list of the given model.
        Args:
        model (str): The name of the model.
        daily (bool): Whether to get the daily forecast (True) or the hourly forecast (False). Defaults to True.
        Returns:
        list[list[float]]: The forecast list of the given model.
        """
        conditions: list[str] = self.condition_list if daily else self.hourly_condition_list
        help_list: list[float] = []
        forecast_list: list[list[float]] = []
        i_range: int = 7 if daily else 42
        time_reference: str = "daily" if daily else "hourly"
        for condition in conditions:
            key = f"{condition}_{model}"
            if key in self.response.json()[time_reference]:
                forecast_list.append(self.response.json()[time_reference][key])
            else:
                for i in range(i_range):
                    help_list.append(None)
                forecast_list.append(help_list)
        return forecast_list

    def get_hourly_forecast(self):
        hourly_best_match_list = self.get_forecast_list(self.model_list[0], daily=False)
        hourly_gem_list = self.get_forecast_list(self.model_list[1], daily=False)
        hourly_gfs_list = self.get_forecast_list(self.model_list[2], daily=False)
        hourly_jma_list = self.get_forecast_list(self.model_list[3], daily=False)
        hourly_icon_list = self.get_forecast_list(self.model_list[4], daily=False)
        hourly_meteofrance_list = self.get_forecast_list(self.model_list[5], daily=False)
        self.hourly_mean_list = self.build_mean(hourly_best_match_list, hourly_gem_list, hourly_gfs_list, hourly_jma_list, hourly_icon_list, hourly_meteofrance_list, self.dates, daily=False)

    def get_daily_forecast(self):
        best_match_list = self.get_forecast_list(self.model_list[0], daily=True)
        gem_list = self.get_forecast_list(self.model_list[1], daily=True)
        gfs_list = self.get_forecast_list(self.model_list[2], daily=True)
        jma_list = self.get_forecast_list(self.model_list[3], daily=True)
        icon_list = self.get_forecast_list(self.model_list[4], daily=True)
        meteofrance_list = self.get_forecast_list(self.model_list[5], daily=True)
        self.daily_mean_list = self.build_mean(best_match_list, gem_list, gfs_list, jma_list, icon_list, meteofrance_list, self.dates, daily=True)

    def get_forecast_icon_name(self, precipitation_probability, cloud_cover, is_day):
        if is_day == 1:
            daytime = "tag"
        else:
            daytime = "nacht"
        
        if precipitation_probability < 25:
            rain_prob = "keine"
        elif 25 <= precipitation_probability < 50:
            rain_prob = "niedrig"
        elif 50 <= precipitation_probability < 75:
            rain_prob = "mittel"
        elif 75 <= precipitation_probability:
            rain_prob = "hoch"

        if cloud_cover < 25:
            clouds = "klar"
        elif 25 <= cloud_cover < 50:
            clouds = "leicht"
        elif 50 <= cloud_cover < 75:
            clouds = "mittel"
        elif 75 <= cloud_cover < 100:
            clouds = "viel"
        elif 100 <= cloud_cover:
            daytime = "tag"
            clouds = "100"
        
        return f"{daytime} {rain_prob} {clouds}"

    def get_wind_direction(self, degree):
        # switching the wind direction from degree to N, S, W, O, ... 
        if degree >= 348 or degree <= 22:
            return "N"
        elif  22 < degree <= 68:
            return "NO"
        elif  68 < degree <= 112:
            return "O"
        elif  112 < degree <= 158:
            return "SO"
        elif  158 < degree <= 202:
            return "S"
        elif  202 < degree <= 248:
            return "SW"
        elif 248 < degree <= 292:
            return "W"
        else:
            return "NW"

    def get_current_weather_values(self):
        self.current_weather = []
        current = self.response.json()["current"]
        
        for condition in self.current_conditions:
            if condition == "wind_direction_10m":
                self.current_weather.append(self.get_wind_direction(int(current[condition])))
            else:
                self.current_weather.append(current[condition])

    def get_date_hour_day_number_and_is_day(self):
        self.dates: list[str] = self.response.json()["daily"]["time"]
        self.is_day: list[str] = self.response.json()["current"]["is_day"]
        current_time = datetime.now()
        self.current_hour = current_time.hour
        todays_day = datetime.today()
        self.todays_number = todays_day.weekday()

    def method_caller(self):
        self.get_date_hour_day_number_and_is_day()
        self.get_current_weather_values()
        self.get_daily_forecast()
        self.get_hourly_forecast()
        
    def get_response(self):
        self.response = requests.get(self.api_adress)

    def render_text(self, text, font, color):
        return font.render(text, 1, color)

    def load_help_text(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
            return text
        except FileNotFoundError:
            print(f"Die Datei {file_path} wurde nicht gefunden.")
            sys.exit()

    def display_help_text(self):
        y_position = 180
        for line in self.text_lines:
            text_surface = self.MAIN_FONT.render(line, True, self.NORMAL_TEXT_COLOR)
            self.WIN.blit(text_surface, (100, y_position))
            y_position += 40

    def check_refresh_button_click(self):
        mouse_pos = pg.mouse.get_pos()
        if self.refresh_button_rect.collidepoint(mouse_pos):
            self.refresh_button_color = self.BUTTON_HOVER_COLOR
            if pg.mouse.get_pressed()[0]:
                self.refresh_button_clicked = True
                self.refresh_button_elevation = 0
                self.response_timer = 27000
            else:
                if self.refresh_button_clicked == True:
                    self.refresh_button_clicked = False
                    self.refresh_button_elevation = 5
        else:
            self.refresh_button_color = self.BUTTON_COLOR
            self.refresh_button_elevation = 5
    
    def check_help_button_click(self):
        mouse_pos = pg.mouse.get_pos()
        if self.help_button_rect.collidepoint(mouse_pos):
            self.help_button_color = self.BUTTON_HOVER_COLOR
            if pg.mouse.get_pressed()[0]:
                self.help_button_clicked = True
                self.help_button_elevation = 0
                self.show_help = True
            else:
                if self.help_button_clicked == True:
                    self.help_button_clicked = False
                    self.help_button_elevation = 5
        else:
            self.help_button_color = self.BUTTON_COLOR
            self.help_button_elevation = 5
        # self.help_text_surf = self.MAIN_FONT.render(self.help_button_text, 1, self.NORMAL_TEXT_COLOR)
        # self.help_text_rect = self.help_text_surf.get_rect(center=self.help_button_rect.center)

    def check_back_button_click(self):
        mouse_pos = pg.mouse.get_pos()
        if self.back_button_rect.collidepoint(mouse_pos):
            self.back_button_color = self.BUTTON_HOVER_COLOR
            if pg.mouse.get_pressed()[0]:
                self.back_button_clicked = True
                self.back_button_elevation = 0
                self.show_help = False
            else:
                if self.back_button_clicked == True:
                    self.back_button_clicked = False
                    self.back_button_elevation = 5
        else:
            self.back_button_color = self.BUTTON_COLOR
            self.back_button_elevation = 5

    def draw_buttons(self):
        if not self.show_help:
            self.refresh_button_rect.y = 80 - self.refresh_button_elevation
            self.refresh_text_rect.center = self.refresh_button_rect.center
            pg.draw.rect(self.WIN, self.BUTTON_SHADOW_COLOR, self.refresh_button_shadow, border_radius= 10)
            pg.draw.rect(self.WIN, self.refresh_button_color, self.refresh_button_rect, border_radius= 10)
            self.WIN.blit(self.refresh_text_surf, self.refresh_text_rect)

            self.help_button_rect.y = 125 - self.help_button_elevation
            self.help_text_rect.center = self.help_button_rect.center
            pg.draw.rect(self.WIN, self.BUTTON_SHADOW_COLOR, self.help_button_shadow, border_radius= 10)
            pg.draw.rect(self.WIN, self.help_button_color, self.help_button_rect, border_radius= 10)
            self.WIN.blit(self.help_text_surf, self.help_text_rect)
        else:
            self.back_button_rect.y = 55 - self.back_button_elevation
            self.back_text_rect.center = self.back_button_rect.center
            pg.draw.rect(self.WIN, self.BUTTON_SHADOW_COLOR, self.back_button_shadow, border_radius= 10)
            pg.draw.rect(self.WIN, self.back_button_color, self.back_button_rect, border_radius= 10)
            self.WIN.blit(self.back_text_surf, self.back_text_rect)
         
    def draw_hourly_forecast_images(self):
        for i in range(16):
            hourly_forecast_icon_string = self.get_forecast_icon_name(float(self.hourly_mean_list[0][i + self.current_hour]), float(self.hourly_mean_list[2][i + self.current_hour]), int(self.hourly_mean_list[6][i + self.current_hour]))
            hourly_forecast_icon = pg.transform.scale(pg.image.load(f"images/{hourly_forecast_icon_string}.png"), (50, 50))
            self.WIN.blit(hourly_forecast_icon, (65 + i * 81, 540))

    def draw_hourly_forecast_text_elements(self):
        for i in range(16):
            forecast_hour = f"{self.current_hour + i}:00" if (self.current_hour + i < 24) else f"{self.current_hour - 24 + i}:00"  # calculate the hour label for 24 hours
            text_to_blit = self.render_text(forecast_hour, self.HOURLY_FONT, self.NORMAL_TEXT_COLOR)  # create the hour label
            self.WIN.blit(text_to_blit, (75 + i * 81, 600))
            for j in range(6):
                text_to_blit = self.render_text(self.hourly_texts[j], self.SMALL_FONT, self.NORMAL_TEXT_COLOR)
                self.WIN.blit(text_to_blit, (45 + i * 81, 633 + j * 20))
                value_color = self.NORMAL_TEXT_COLOR
                if j == 0:
                    if int(self.hourly_mean_list[j][i + self.current_hour]) > 75:
                        value_color = self.RED
                    elif 75 >= int(self.hourly_mean_list[j][i + self.current_hour]) > 50:
                        value_color = self.ORANGE
                    elif 50 >= int(self.hourly_mean_list[j][i + self.current_hour]) > 25:
                        value_color = self.YELLOW
                text_to_blit = self.render_text(str(self.hourly_mean_list[j][i + self.current_hour]), self.HOURLY_FONT, value_color)
                self.WIN.blit(text_to_blit, (75 + i * 81, 630 + j * 20))

    def draw_daily_forecast_images(self):
        for i in range(7):
            percent_daylight = round(float(self.daily_mean_list[7][i]) * 100 / float(self.daily_mean_list[6][i]), 2)
            daily_forecast_icon_string = self.get_forecast_icon_name(int(self.daily_mean_list[8][i]), 100-percent_daylight, 1)  # calculating cloud cover
            daily_forecast_icon = pg.transform.scale(pg.image.load(f"images/{daily_forecast_icon_string}.png").convert_alpha(), (80, 80))
            self.WIN.blit(daily_forecast_icon, (520 + i * 110, 80))
            
    def draw_daily_forecast_text_elemets(self):
        for a, attribute in enumerate(self.forecast_texts):
            text_to_blit = self.render_text(attribute, self.MAIN_FONT, self.NORMAL_TEXT_COLOR)
            self.WIN.blit(text_to_blit, (300, 200 + a * 30))
        for u, unit in enumerate(self.weather_units):
            text_to_blit = self.render_text(unit, self.MAIN_FONT, self.NORMAL_TEXT_COLOR)
            self.WIN.blit(text_to_blit, (1285, 200 + u * 30))

        for i in range(7):
            for j in range(10):
                if j == 0:  # this is the date
                    value_to_blit = self.render_text(self.change_date_format(self.daily_mean_list[j][i]), self.MAIN_FONT, self.NORMAL_TEXT_COLOR)
                elif j == 4 :  # this is the wind direction
                    value_to_blit = self.render_text(self.get_wind_direction(int(self.daily_mean_list[j][i])), self.MAIN_FONT, self.NORMAL_TEXT_COLOR)
                elif j == 6 or j == 7:  # both are given in seconds -> calculate hours
                    value_to_blit = self.render_text(str((round(self.daily_mean_list[j][i] / 60 / 60, 2))), self.MAIN_FONT, self.NORMAL_TEXT_COLOR)
                else:
                    value_to_blit = self.render_text(str(self.daily_mean_list[j][i]), self.MAIN_FONT, self.NORMAL_TEXT_COLOR)
                x_position = 520 if j == 0 else 548
                self.WIN.blit(value_to_blit, (x_position + i * 110, 200 + j * 30))

            if self.todays_number + i > 6:
                idx = self.todays_number + i - 7
            else:
                idx = self.todays_number + i
            x_cord = 530 if idx != 3 else 520
            day_text = self.days_in_german[idx] if idx != self.todays_number else "  Heute"
            text_to_blit = self.render_text(day_text, self.MAIN_FONT, self.NORMAL_TEXT_COLOR)
            self.WIN.blit(text_to_blit, (x_cord + i * 110, 170))
            # print(f"{float(self.daily_mean_list[7][i])} : {float(self.daily_mean_list[6][i])} : {float(self.daily_mean_list[8][i])} : {percent_daylight}")

    def draw_current_weather_icon(self):
        # 25 mm precipitation is the highest normal value in germany, so this is assumed to be 100%
        precipitation_in_percent = round(float(self.current_weather[1]) * 100 / 25, 2)
        current_icon_name = self.get_forecast_icon_name(precipitation_in_percent, float(self.current_weather[0]), self.is_day)
        current_icon_image = pg.image.load(f"images/{current_icon_name}.png").convert_alpha()
        self.WIN.blit(current_icon_image, (50, 50))

    def draw_current_weather_values(self):
        for i in range(5):
            value_to_blit = self.render_text(self.current_weather_texts[i], self.MAIN_FONT, self.NORMAL_TEXT_COLOR)
            self.WIN.blit(value_to_blit, (50, 300 + i * 30))
            value_to_blit = self.render_text(str(self.current_weather[i]), self.MAIN_FONT, self.NORMAL_TEXT_COLOR)
            self.WIN.blit(value_to_blit, (170, 300 + i * 30))
            value_to_blit = self.render_text(self.current_weather_units[i], self.MAIN_FONT, self.NORMAL_TEXT_COLOR)
            self.WIN.blit(value_to_blit, (210, 300 + i * 30))

    def draw_icon_surfaces(self):
        pg.draw.rect(self.WIN, self.SYMBOL_RECT_COLOR, (55, 55, 182, 182), border_radius=15)
        for i in range(7):
            pg.draw.rect(self.WIN, self.SYMBOL_RECT_COLOR, (522 + i * 110, 82, 76, 76), border_radius=13)
        for i in range(16):
            pg.draw.rect(self.WIN, self.SYMBOL_RECT_COLOR, (66 + i * 81, 541, 48, 48), border_radius=11)

    def draw_icon_surface_accents(self):
        pg.draw.rect(self.WIN, self.ACCENT_COLOR, (50, 50, 192, 192), border_radius=15)
        for i in range(7):
            pg.draw.rect(self.WIN, self.ACCENT_COLOR, (520 + i * 110, 80, 80, 80), border_radius=13)
        for i in range(16):
            pg.draw.rect(self.WIN, self.ACCENT_COLOR, (65 + i * 81, 540, 50, 50), border_radius=11)

    def draw_seperators(self):
        pg.draw.line(self.WIN, self.SEPARATOR_COLOR, (280, 50), (280, 495))
        pg.draw.line(self.WIN, self.SEPARATOR_COLOR, (1330, 225), (1330, 315))
        pg.draw.line(self.WIN, self.SEPARATOR_COLOR, (1330, 345), (1330, 465))
        pg.draw.line(self.WIN, self.SEPARATOR_COLOR, (50, 623), (1330, 623))
        for i in range(11):
            end = 1275 if i < 1 or i > 9 else 1330
            start = 280 if i < 10 else 50
            pg.draw.line(self.WIN, self.SEPARATOR_COLOR, (start, 195 + i * 30), (end, 195 + i * 30))
        for i in range(8):
            pg.draw.line(self.WIN, self.SEPARATOR_COLOR, (507 + i * 110, 195), (507 + i * 110, 495))
        for i in range(15):
            pg.draw.line(self.WIN, self.SEPARATOR_COLOR, (120 + i * 81, 600), (120 + i * 81, 732))

    def draw_headings_and_legend(self):
        text_to_blit = self.render_text("6-Tage-Vorhersage", self.HEADING_FONT, self.NORMAL_TEXT_COLOR)
        self.WIN.blit(text_to_blit, (632, 35))
        text_to_blit = self.render_text("Aktuelles Wetter", self.HEADING_FONT, self.NORMAL_TEXT_COLOR)
        self.WIN.blit(text_to_blit, (50, 260))
        text_to_blit = self.render_text("Stündliche Wettervorhersage",self.HEADING_FONT, self.NORMAL_TEXT_COLOR)
        self.WIN.blit(text_to_blit, (65, 500))
        text_to_blit = self.render_text("Nw = Niederschlagswahrscheinlichkeit in %  |  Ns = Niederschlagshöhe in mm  |  Wd = Wolkendecke in %  |  Ld = Luftdruckdefizit in kPa  |  Te = Temperatur in °C  |  uv = UV-Index", self.SMALL_FONT, self.NORMAL_TEXT_COLOR)
        self.WIN.blit(text_to_blit, (250, 758))

    def draw_underlines(self):
        pg.draw.line(self.WIN, self.UNDERLINE_COLOR, (632, 63), (842,63), 2)
        pg.draw.line(self.WIN, self.UNDERLINE_COLOR, (50, 288), (242,288), 2)
        pg.draw.line(self.WIN, self.UNDERLINE_COLOR, (65, 528), (389,528), 2)

    def draw_window(self):
        self.WIN.fill(self.BACKGROUND_COLOR)
        if not self.show_help:
            self.draw_underlines()
            self.draw_headings_and_legend()
            self.draw_icon_surface_accents()
            self.draw_icon_surfaces()
            self.draw_seperators()
            self.draw_current_weather_values()
            self.draw_current_weather_icon()
            self.draw_daily_forecast_text_elemets()
            self.draw_daily_forecast_images()
            self.draw_hourly_forecast_text_elements()
            self.draw_hourly_forecast_images()
        else:
            self.help_text = self.load_help_text(self.help_file_path)
            self.text_lines = self.help_text.splitlines()
            self.display_help_text()

        self.draw_buttons()
        pg.display.update()

    def main(self):
        run = True
        self.response_timer = 27000
        while run:
            self.response_timer += 1

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

            if self.response_timer >= 27000:
                self.response_timer = 0
                self.get_response()
                self.method_caller()

            self.draw_window()
            self.check_refresh_button_click()
            self.check_help_button_click()
            self.check_back_button_click()
            self.clock.tick(self.FPS)
        
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    weather_app = WeatherApp()
    weather_app.main()