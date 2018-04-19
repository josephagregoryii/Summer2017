from os import chdir
from os.path import dirname, realpath
import csv

from flask import Flask, render_template, send_from_directory, request, redirect
from math import ceil

app = Flask(__name__)

PER_PAGE = 10


# DEMO STUFF

class Pagination(object):
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
                    (num > self.page - left_current - 1 and \
                                 num < self.page + right_current) or \
                            num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


class Post:
    def __init__(self, list):
        self._post_id = list[0]
        self._handle = list[1]
        self._postDate = list[2]
        self._postType = list[3]
        self._gen_postType = list[4]
        self._postUrl = list[5]
        self._platform = list[6]
        self._message = list[7]
        self._twitter_comment = list[8]
        self._twitter_retweet = list[9]
        self._relevant_prediction = list[10]
        self._cta_prediction = list[11]
        self._sell_prediction = list[12]
        self._intent_prediction = list[13]
        self._comments = list[14]
        self._shares = list[15]
        self._likes = list[16]
        self._views = list[17]
        self._campaignId = list[18]
        self._campaign_name = list[19]
        self._campaign_startDate = list[20]
        self._campaign_endDate = list[21]
        self._project_currency = list[22]
        self._project_staffPick = list[23]
        self._sub_category = list[24]
        self._categorynames = list[25]
        self._categorynumbers = list[26]
        self._project_url = list[27]
        self._project_backerCount = list[28]
        self._project_goal = list[29]
        self._project_pledgeAmount = list[30]
        self._succeeded = list[31]
        self._imageUrl = list[32]


class Campaign:
    def __init__(self, list):
        self._campaignId = list[18]
        self._campaign_name = list[19]
        self._campaign_startDate = list[20]
        self._campaign_endDate = list[21]
        self._project_currency = list[22]
        self._project_staffPick = list[23]
        self._sub_category = list[24]
        self._categorynames = list[25]
        self._categorynumbers = list[26]
        self._project_url = list[27]
        self._project_backerCount = list[28]
        self._project_goal = list[29]
        self._project_pledgeAmount = list[30]
        self._succeeded = list[31]

        initial_post = Post(list)
        self._listOfPosts = []
        self._listOfPosts.append(initial_post)

    def addPost(self, post):
        self._listOfPosts.append(post)
        return self._listOfPosts

#RECURSIVE
posttype_results = []
def search_by_posttype(list, postType):  # filter by post 5
    global posttype_results
    if postType == '':
        return list
    else:
        if len(list) > 3000:
            div = len(list)//2
            front = list[:div]
            back = list[div:]
            search_by_posttype(front,postType)
            search_by_posttype(back,postType)
        else:
            if postType =='10':
                postType = 'text'
            for post in list:
                if str(post._gen_postType) == str(postType):
                    posttype_results.append(post)
        return posttype_results

platform_result = []
def search_by_platform(list, platform):  # filter by post 4
    global platform_result
    if platform == '':
        return list
    else:
        if len(list) > 3000:
            div = len(list) // 2
            front = list[:div]
            back = list[div:]
            search_by_platform(front,platform)
            search_by_platform(back,platform)
        else:
            for post in list:
                if str(post._platform) == str(platform):
                    platform_result.append(post)
        return platform_result
bool = False
success_list = []
def search_by_success(list, success):  # filter by campaign 1
    global success_list
    global bool
    if success == 2:
        bool = True
        base = [y for x in list for y in x._listOfPosts]
        return base
    else:
        if len(list) > 1000:
            div = len(list)//2
            front = list[:div]
            back = list[div:]
            bool = True
            search_by_success(front,success)
            search_by_success(back,success)
        else:
            bool = True
            for campaign in list:
                if int(campaign._succeeded) == int(success):
                    for x in campaign._listOfPosts:
                        success_list.append(x)
        return success_list

intent_results = []
def search_by_intent(list, intent):  # filter by post 3
    global intent_results
    global bool
    if intent == '' and bool == False:
        bool = True
        base = [y for x in list for y in x._listOfPosts]
        return base
    elif intent == '':
        return list
    else:
        if len(list) > 3000:
            div = len(list)//2
            front = list[:div]
            back = list[div:]
            search_by_intent(front,intent)
            search_by_intent(back,intent)
        else:
            for campaign in list:
                    if int(campaign._intent_prediction) == int(intent):
                        intent_results.append(campaign)
        return intent_results

category_results = []
def search_by_category(list, category):  # filter by campaign 2
    global category_results
    global bool
    if category == '' and bool == False:
        bool = True
        base = [y for x in list for y in x._listOfPosts]
        return base
    elif category == '':
        return list
    else:
        if len(list) > 3000:
            half = len(list)//2
            front = list[:half]
            back = list[half:]
            search_by_category(front,category)
            search_by_category(back,category)
        else:
            for campaign in list:
                if str(campaign._categorynames) == str(category):
                    category_results.append(campaign)
        return category_results

def get_data():
    listOfCampaigns = []
    listofcid = []
    prev_obj = None
    global full_list
    contents = []

    global full_list
    with open('data1.csv', errors='ignore') as csvfile1:
        reader1 = csv.reader(csvfile1)
        for row1 in reader1:
            contents.append(row1)
    with open('data2.csv', errors='ignore') as csvfile2:
        reader2 = csv.reader(csvfile2)
        for row2 in reader2:
            contents.append(row2)
    with open('data3.csv', errors='ignore') as csvfile3:
        reader3 = csv.reader(csvfile3)
        for row3 in reader3:
            contents.append(row3)
    with open('data4.csv', errors='ignore') as csvfile4:
        reader4 = csv.reader(csvfile4)
        for row4 in reader4:
            contents.append(row4)
    with open('data5.csv', errors='ignore') as csvfile5:
        reader5 = csv.reader(csvfile5)
        for row5 in reader5:
            contents.append(row5)
    tables = contents[0]

    for row in contents[1:]:
        temp = []
        cells = row
        post_id = cells[1]
        handle = cells[2]
        postDate = cells[3]
        postType = cells[4]
        gen_postType = cells[5]
        postUrl = cells[6]
        platform = cells[7]
        message = cells[8]
        twitter_comment = cells[9]
        twitter_retweet = cells[10]
        relevant_prediction = cells[11]
        cta_prediction = cells[12]
        sell_prediction = cells[13]
        intent_prediction = cells[14]
        comments = cells[15]
        shares = cells[16]
        likes = cells[17]
        views = cells[18]
        campaignId = cells[19]
        campaign_name = cells[20]
        campaign_startDate = cells[21]
        campaign_endDate = cells[22]
        project_currency = cells[23]
        project_staffPick = cells[24]
        sub_category = cells[25]
        categorynames = cells[26]
        categorynumbers = cells[27]
        project_url = cells[28]
        project_backerCount = cells[29]
        project_goal = cells[30]
        project_pledgeAmount = cells[31]
        succeeded = cells[32]
        imageUrl = cells[33]

        temp.append(post_id)
        temp.append(handle)
        temp.append(postDate)
        temp.append(postType)
        temp.append(gen_postType)
        temp.append(postUrl)
        temp.append(platform)
        temp.append(message)
        temp.append(twitter_comment)
        temp.append(twitter_retweet)
        temp.append(relevant_prediction)
        temp.append(cta_prediction)
        temp.append(sell_prediction)
        temp.append(intent_prediction)
        temp.append(comments)
        temp.append(shares)
        temp.append(likes)
        temp.append(views)
        temp.append(campaignId)
        temp.append(campaign_name)
        temp.append(campaign_startDate)
        temp.append(campaign_endDate)
        temp.append(project_currency)
        temp.append(project_staffPick)
        temp.append(sub_category)
        temp.append(categorynames)
        temp.append(categorynumbers)
        temp.append(project_url)
        temp.append(project_backerCount)
        temp.append(project_goal)
        temp.append(project_pledgeAmount)
        temp.append(succeeded)
        temp.append(imageUrl)

        temp_post = Post(temp)

        if prev_obj == None:
            obj = Campaign(temp)
            prev_obj = obj
            listofcid.append(campaignId)
            listOfCampaigns.append(obj)
        elif prev_obj._campaignId == campaignId:
            prev_obj.addPost(temp_post)
        else:
            obj = Campaign(temp)
            listofcid.append(campaignId)
            prev_obj = obj
            listOfCampaigns.append(prev_obj)

    listOfCampaigns.append(prev_obj)
    return listOfCampaigns

print("Retrieving data...")
campaign_list = get_data()
print("Data Retrieved")
searched_list = []
total_pages = 0
searched = False

def delete():
    global posttype_results
    global platform_result
    global success_list
    global intent_results
    global category_results
    del posttype_results[:]
    del platform_result[:]
    del success_list[:]
    del intent_results[:]
    del category_results[:]

@app.route('/', methods=['GET', 'POST'])
def view_root():
    global searched_list
    global searched
    global total_pages
    page = 1
    startFrom = (page - 1) * PER_PAGE
    endOn = page * PER_PAGE

    searched = False
    searched_list = []
    total_pages = 1

    lst = []
    return render_template('base.html', result_list=lst, startFrom=startFrom, endOn=endOn, page_num=1,
                           total_pages=total_pages)

list=[]
@app.route('/page/<int:page>', methods=['GET', 'POST'])
def view_page(page):
    global campaign_list
    global searched_list
    global searched
    global total_pages
    myList = [request.args.get('succeeded'), request.args.get('category'), request.args.get('postType'),
              request.args.get('platform'), request.args.get('intent')]
    startFrom = (page - 1) * PER_PAGE
    endOn = page * PER_PAGE
    if all(myList[0] == x for x in myList) and searched == False:
        pagination = Pagination(page, PER_PAGE, count)
        return render_template('base.html', result_list=lst)
    elif searched == False:
        searched = True
        delete()
        success_results = search_by_success(campaign_list, int(request.args.get('succeeded')))
        category_list = search_by_category(success_results, str(request.args.get('category')))
        intent_list = search_by_intent(category_list, int(request.args.get('intent')))
        platform_results = search_by_platform(intent_list, request.args.get('platform'))
        postType_results = search_by_posttype(platform_results, str(request.args.get('postType')))
        searched_list = postType_results
        total_pages = int(ceil(len(searched_list) / float(PER_PAGE)))
        lst = searched_list
        return render_template('base.html', result_list=lst)
    else:
        lst = searched_list
        return render_template('base.html', result_list=lst)

@app.route('/<id>')
def view_post(id):
    for index in range(len(searched_list)):
        if searched_list[index]._post_id == id:
            current_post = searched_list[index]
            if index == 0:
                before_post_id = 0
            else:
                before_post_id = searched_list[index - 1]._post_id

            if index == len(searched_list) - 1:
                after_post_id = 0
            else:
                after_post_id = searched_list[index + 1]._post_id
            return render_template('post.html', post=current_post, before_id=before_post_id, after_id=after_post_id)
    return "ok"


# DON'T TOUCH THE CODE BELOW THIS LINE
@app.route('/css/<file>')
def view_css(file):
    return send_from_directory('css', file)

@app.route('/js/<file>')
def get_js(file):
    return send_from_directory('js', file)

if __name__ == '__main__':
    chdir(dirname(realpath(__file__)))
    app.run(debug=True)
