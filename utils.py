from flask import session, session, flash, redirect, url_for, render_template

def get_page(total, p):
	show_page = 6      		   # 显示的页码数
	pageoffset = 3             # 偏移量
	start = 1                  #分页条开始
	end = total                #分页条结束

	if total > show_page:
		if p > pageoffset:
			start = p - pageoffset
			if total > p + pageoffset:
				end = p + pageoffset
			else:
				end = total
		else:
			start = 1
			if total > show_page:
				end = show_page
			else:
				end = total
		if p + pageoffset > total:
			start = start - (p + pageoffset - end)
	print('total - page - showpage - start - end: {} - {} - {} - {} - {}'.format(total,p, show_page,start,end))
	dic = range(start, end + 1)
	return dic

from functools import wraps
def require_login(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        if not 'username' in session:
            flash('Please login system firstly!', 'danger')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return inner_func
