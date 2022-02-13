
# I ran "sudo apt-get install python3-tk" to get tkinter, might be different on your system, comes with anaconda
# "pip install requests" to download the requests module on your system

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import db_api
import html_util

class GUI:
	tk_window = tk.Tk()

	login_frame = ttk.Frame(tk_window)
	create_account_frame = ttk.Frame(tk_window)
	main_frame = ttk.Frame(tk_window)
	submit_article_frame = ttk.Frame(tk_window)
	specific_location_frame = ttk.Frame(tk_window)

	username_tk_input = tk.StringVar()
	password_tk_input = tk.StringVar()
	location_tk_input = tk.StringVar()
	account_create_input_email = tk.StringVar()
	account_create_input_password= tk.StringVar()
	account_create_input_city = tk.StringVar()
	account_create_input_country = tk.StringVar()
	sumbit_article_input_website = tk.StringVar()
	submit_article_input_link = tk.StringVar()
	sumbit_article_is_homepage = tk.StringVar()

	main_page_tree_view = ttk.Treeview(main_frame, columns=(1,2,3), show="headings")
	specific_homepage_tree = ttk.Treeview(specific_location_frame, columns=(1,2), show="headings")
	specific_non_homepage_tree = ttk.Treeview(specific_location_frame, columns=(1,2), show="headings")
	specific_national_news_tree = ttk.Treeview(specific_location_frame, columns=(1,2), show="headings")


	logged_in_user = ""

	country_codes = ['ar', 'gr', 'nl', 'za', 'au', 'hk', 'nz', 'kr', 'at',
	'hu', 'ng', 'se', 'be', 'in', 'no', 'ch', 'br', 'id', 'ph', 'tw', 'bg', 'ie', 'pl',
	'th', 'ca', 'il', 'pt', 'tr', 'cn', 'it', 'ro', 'ae', 'co', 'jp', 'ru', 'ua', 'cu',
	'lv', 'sa', 'gb','cz', 'lt', 'rs', 'us', 'eg', 'my', 'sg', 've', 'fr', 'mx', 'sk',
	 'de', 'ma', 'si']

	db = db_api.DatabaseAccessor()

	def __init__(self):
		self.tk_window.geometry("600x700")
		self.tk_window.resizable(True, True)
		self.tk_window.title('GUTS')
		
		self.__login_frame_init()

	## login callbacks

	def __login_frame_login_btn(self):

		success = self.db.check_login(self.username_tk_input.get(), self.password_tk_input.get())
		
		if(success):
			self.logged_in_user = self.username_tk_input.get()
			self.login_frame.destroy()
			self.__main_frame_init()
		else:
			msg = f'Invalid Login!'
			showinfo(title='Failed', message=msg)

	def __login_frame_init(self):
		self.login_frame = ttk.Frame(self.tk_window)
		self.login_frame.pack(padx=20, pady=20, fill='x', expand=True)

		_label = ttk.Label(self.login_frame, 
			text=f"Login to GlobalTouch or create an account",
			font=("TkDefaultFont", 12))
		_label.pack()

		username_label = ttk.Label(self.login_frame, text="Username:")
		username_label.pack(fill='x', expand=True)

		username_box = ttk.Entry(self.login_frame, textvariable=self.username_tk_input)
		username_box.pack(fill='x', expand=True)
		username_box.focus()

		password_label = ttk.Label(self.login_frame, text="Password:")
		password_label.pack(fill='x', expand=True)

		password_box = ttk.Entry(self.login_frame, textvariable=self.password_tk_input, show='*')
		password_box.pack(fill='x', expand=True)
		password_box.focus()

		login_button = ttk.Button(self.login_frame, text="Login", command=self.__login_frame_login_btn)
		login_button.pack(fill='x', expand=True, pady=10)

		login_button = ttk.Button(self.login_frame, text="Create Account", command=self.__login_frame_create_account_btn)
		login_button.pack(fill='x', expand=True, pady=10)

	def __login_frame_create_account_btn(self):
		self.login_frame.destroy()
		self.__create_account_frame_init()

	##create account callbacks

	def __create_account_frame_create_account_btn(self):
		if( self.username_tk_input.get() != "" and 
			self.account_create_input_email.get() != "" and
			self.account_create_input_password.get() != "" and
			self.account_create_input_city.get() != ""):

			if(self.country_codes.count(self.account_create_input_country.get()) > 0):

				msg = f'Added username {self.username_tk_input.get()} to the database!'
				showinfo(title='Success', message=msg)

				self.db.add_user(self.username_tk_input.get(), 
						self.account_create_input_password.get(),
						self.account_create_input_email.get(),
						self.account_create_input_city.get(),
						self.account_create_input_country.get(),)
		
				self.create_account_frame.destroy()
				self.__login_frame_init()
			
			else:
				msg = f'Incorrect Country Code (check the country code link)!'
				showinfo(title='Failed', message=msg)
		else:
			msg = f'Missing Fields!'
			showinfo(title='Failed', message=msg)

	
	def __create_account_frame_back_btn(self):
		self.create_account_frame.destroy()
		self.__login_frame_init()

	def __create_account_frame_init(self):
		self.create_account_frame = ttk.Frame(self.tk_window)
		self.create_account_frame.pack(padx=20, pady=20, fill='x', expand=True)

		username_label = ttk.Label(self.create_account_frame, text="Username:")
		username_label.pack(fill='x', expand=True)

		username_box = ttk.Entry(self.create_account_frame, textvariable=self.username_tk_input)
		username_box.pack(fill='x', expand=True)
		username_box.focus()

		email_label = ttk.Label(self.create_account_frame, text="Email:")
		email_label.pack(fill='x', expand=True)

		email_box = ttk.Entry(self.create_account_frame, textvariable=self.account_create_input_email)
		email_box.pack(fill='x', expand=True)
		email_box.focus()

		password_label = ttk.Label(self.create_account_frame, text="Password:")
		password_label.pack(fill='x', expand=True)

		password_box = ttk.Entry(self.create_account_frame, textvariable=self.account_create_input_password, show='*')
		password_box.pack(fill='x', expand=True)
		password_box.focus()

		city_label = ttk.Label(self.create_account_frame, text="City:")
		city_label.pack(fill='x', expand=True)

		city_box = ttk.Entry(self.create_account_frame, textvariable=self.account_create_input_city)
		city_box.pack(fill='x', expand=True)
		city_box.focus()

		country_label = ttk.Label(self.create_account_frame, text="Country Code(https://newsapi.org/sources):")
		country_label.pack(fill='x', expand=True)

		country_box = ttk.Entry(self.create_account_frame, textvariable=self.account_create_input_country)
		country_box.pack(fill='x', expand=True, pady=10)

		create_account_btn = ttk.Button(self.create_account_frame, text="Create Account", command=self.__create_account_frame_create_account_btn)
		create_account_btn.pack(fill='x', expand=True, pady=15)

		create_account_back_btn = ttk.Button(self.create_account_frame, text="Back", command=self.__create_account_frame_back_btn)
		create_account_back_btn.pack(fill='x', expand=True, pady=15)

	## main frame callbacks

	def __main_frame_get_news_btn(self):
		self.main_frame.destroy()
		self.__specific_country_init()

	def __main_frame_to_login_btn(self):
		self.main_frame.destroy()
		self.__login_frame_init()

	def __main_frame_submit_btn(self):
		self.main_frame.destroy()
		self.__submit_article_frame_init()

	def __main_frame_tree_view_selected(self, event):
		item = self.main_page_tree_view.selection()[0]

		html_util.open_url(self.main_page_tree_view.item(item, "values")[1])

	def __main_frame_init(self):
		self.main_frame = ttk.Frame(self.tk_window)

		self.main_frame.pack(padx=0, pady=0, fill='x', expand=True, side=tk.TOP)

		_label = ttk.Label(self.main_frame, text=f"Articles shared from co-workers:", font=("TkDefaultFont", 14))
		_label.pack(pady=10)

		submit_btn = ttk.Button(self.main_frame, text="Submit An Article",command=self.__main_frame_submit_btn, width=20)
		submit_btn.pack(side=tk.TOP, pady=20)


		user = self.db.get_user_by_name(self.logged_in_user)
		rows = self.db.get_websites_from_other_countries(self.db.city_code_to_country_name(user.cityCode), False)

		self.main_page_tree_view = ttk.Treeview(self.main_frame, columns=(1,2,3), show="headings", height=len(rows))
		self.main_page_tree_view.bind('<Double-1>', self.__main_frame_tree_view_selected)
		self.main_page_tree_view.heading(1, text="Title")
		self.main_page_tree_view.heading(2, text="Link")
		self.main_page_tree_view.heading(3, text="Country")
		for i in rows:
			self.main_page_tree_view.insert('', "end", values=[i.name, i.link, self.db.country_code_to_name(i.countryCode)])
		self.main_page_tree_view.pack(expand=tk.YES, fill=tk.BOTH)

		
		title_label = ttk.Label(self.main_frame, text="\n\nSpecific City Info:", anchor="center", font=("TkDefaultFont", 14))
		title_label.pack(fill='x', expand=True)

		cities = self.db.get_all_cities()

		cities.append(cities[0])
		self.location_tk_input.set(cities[0])
		tk_option_menu = ttk.OptionMenu(self.main_frame, self.location_tk_input, *cities)
		tk_option_menu.pack()

		select_btn = ttk.Button(self.main_frame, text="Get Info",command=self.__main_frame_get_news_btn, width=20)
		select_btn.pack(fill='x', expand=False, pady=10)

	## specific country callbacks

	def __specific_location_back_btn(self):
		self.specific_location_frame.destroy()
		self.__main_frame_init()

	def __specific_frame_homepage_view_selected(self, event):
		item = self.specific_homepage_tree.selection()[0]

		html_util.open_url(self.specific_homepage_tree.item(item, "values")[1])
	
	def __specific_frame_non_homepage_view_selected(self, event):
		item = self.specific_non_homepage_tree.selection()[0]

		html_util.open_url(self.specific_non_homepage_tree.item(item, "values")[1])
	
	def __specific_frame_national_news_view_selected(self, event):
		item = self.specific_national_news_tree.selection()[0]

		html_util.open_url(self.specific_national_news_tree.item(item, "values")[1])


	def __specific_country_init(self):
		self.specific_location_frame = tk.Frame(self.tk_window)
		self.specific_location_frame.pack(padx=0, pady=0, fill='x', expand=True, side=tk.TOP)

		back_btn = ttk.Button(self.specific_location_frame, text="Back",command=self.__specific_location_back_btn)
		back_btn.pack(fill='x', expand=False, pady=10)

		country = self.db.city_name_to_country_name(self.location_tk_input.get())

		_label = ttk.Label(self.specific_location_frame, 
			text=f"{self.location_tk_input.get()} Weather",
			font=("TkDefaultFont", 14))
		_label.pack()

		_label = ttk.Label(self.specific_location_frame, text=f"The weather is {html_util.weather(self.location_tk_input.get())}\nThe temperature is {html_util.temp(self.location_tk_input.get())} °C\n\n")
		_label.pack()

		_label = ttk.Label(self.specific_location_frame, text=f"News:", font=("TkDefaultFont", 14))
		_label.pack()


		homepageRows = self.db.get_websites_from_country(country, True)

		if len(homepageRows) != 0:
			_label = ttk.Label(self.specific_location_frame, text=f"\nlocal employee homepages:")
			_label.pack()
			self.specific_homepage_tree = ttk.Treeview(self.specific_location_frame, columns=(1,2), show="headings", height=len(homepageRows))
			self.specific_homepage_tree.heading(1, text="Newspage")
			self.specific_homepage_tree.heading(2, text="Link")
			for i in homepageRows:
				self.specific_homepage_tree.insert('', "end", values=[i.name, i.link])
			self.specific_homepage_tree.pack(expand=tk.YES, fill=tk.BOTH)
			self.specific_homepage_tree.bind('<Double-1>', self.__specific_frame_homepage_view_selected)

		
		articleRows = self.db.get_websites_from_country(country, False)
		if len(articleRows) != 0:
			_label = ttk.Label(self.specific_location_frame, text=f"\nlocal employee articles:")
			_label.pack()

			self.specific_non_homepage_tree = ttk.Treeview(self.specific_location_frame, columns=(1,2), show="headings", height=len(articleRows))
			self.specific_non_homepage_tree.heading(1, text="Newspage")
			self.specific_non_homepage_tree.heading(2, text="Title")
			#self.specific_non_homepage_tree.heading(3, text="Link")
			for i in articleRows:
				#self.specific_non_homepage_tree.insert('', "end", values=[i.name, html_util.get_page_title(i.link), i.link])
				self.specific_non_homepage_tree.insert('', "end", values=[i.name, i.link])
			self.specific_non_homepage_tree.pack(expand=tk.YES, fill=tk.BOTH)
			self.specific_non_homepage_tree.bind('<Double-1>', self.__specific_frame_non_homepage_view_selected)

		_label = ttk.Label(self.specific_location_frame, text=f"\nnational headlines:")
		_label.pack()

		online = html_util.list_of_articles(self.db.city_name_to_country_name(self.location_tk_input.get()))

		if len(online) != 0:
			self.specific_national_news_tree = ttk.Treeview(self.specific_location_frame, columns=(1,2), show="headings", height=len(online))
			self.specific_national_news_tree.heading(1, text="Newspage")
			self.specific_national_news_tree.heading(2, text="Link")
			for i in online:
				self.specific_national_news_tree.insert('', "end", values=[i[0],i[1]])
			self.specific_national_news_tree.pack(expand=tk.YES, fill=tk.BOTH)
			self.specific_national_news_tree.bind('<Double-1>', self.__specific_frame_national_news_view_selected)

	## submit article callbacks

	def __sumbit_article_back_btn(self):
		self.submit_article_frame.destroy()
		self.__main_frame_init()

	def __sumbit_article_submit_btn(self):
		self.submit_article_frame.destroy()

		user = self.db.get_user_by_name(self.logged_in_user)

		ishomepage = False
		if(self.sumbit_article_is_homepage.get() == "yes"):
			ishomepage = True

		self.db.add_website(
			self.sumbit_article_input_website.get(),
		    ishomepage, 
			self.submit_article_input_link.get(), 
			self.db.city_code_to_country_name(user.cityCode))

		msg = f'Added website to registry'
		showinfo(title='Success', message=msg)

		self.__main_frame_init()


	def __submit_article_frame_init(self):
		self.submit_article_frame = ttk.Frame(self.tk_window)
		self.submit_article_frame.pack(padx=20, pady=20, fill='x', expand=True)

		name_label = ttk.Label(self.submit_article_frame, text="Website Name:")
		name_label.pack(fill='x', expand=True)

		name_box = ttk.Entry(self.submit_article_frame, textvariable=self.sumbit_article_input_website)
		name_box.pack(fill='x', expand=True)
		name_box.focus()

		email_label = ttk.Label(self.submit_article_frame, text="Website Link:")
		email_label.pack(fill='x', expand=True)

		email_box = ttk.Entry(self.submit_article_frame, textvariable=self.submit_article_input_link)
		email_box.pack(fill='x', expand=True)
		email_box.focus()

		is_homepage = ttk.Checkbutton(self.submit_article_frame,
                text='Homepage:',
                variable=self.sumbit_article_is_homepage,
                onvalue='yes',
                offvalue='no').pack()

		submit_btn = ttk.Button(self.submit_article_frame, text="Submit Article", command=self.__sumbit_article_submit_btn)
		submit_btn.pack(fill='x', expand=True, pady=10)

		back_btn = ttk.Button(self.submit_article_frame, text="Back", command=self.__sumbit_article_back_btn)
		back_btn.pack(fill='x', expand=True, pady=10)


	def run(self):
		self.tk_window.mainloop()


gui = GUI()

gui.run()