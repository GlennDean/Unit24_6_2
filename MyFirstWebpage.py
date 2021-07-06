from flask import Flask, redirect, url_for, render_template, request, session
import pickle

app = Flask(__name__)
app.secret_key = "lm17"

corr_mat = pickle.load( open( "save_corr_mat.p", "rb" ) )
book_list = pickle.load( open( "save_book_list.p", "rb" ) )
book_names = pickle.load( open( "save_book_names.p", "rb" ) )

num_books_in_list = len(book_list)
max_books_to_display = 20

# sort a list of tuples on the 2nd element
def Sort_Tuple(tup): 
  
    # reverse = None (Sorts in Ascending order) 
    # key is set to sort using second element of 
    # sublist lambda has been used 
    tup.sort(key = lambda x: x[1],reverse = True) 
    return tup 

# book_name ==> index into book_names list
def get_index_for_book(book_name):
    for i in range(num_books_in_list):
        if book_names[i] == book_name:
            return i

    return -1

# book_name ==> ordered list of tuples, with descending
# values of cosine-similarity (each ordered tuple is of the form
# (book name,cos-sim value)
def get_ordered_list_for_book(book_name):
    ordered_list = []
    idx = get_index_for_book(book_name)
    if (idx < 0):
        return ordered_list
    unordered_list = [(book_names[i],corr_mat[idx,i]) for i in range(len(book_names))]
    
    ordered_list = Sort_Tuple(unordered_list)

    return ordered_list

# book_name ==> index of a book in book_names that is closest
# to book_name
def get_first_index_closes_to_name(book_name):
    # IMPORTANT - search for names that match "the longest" (that is,
    # try to find a match on 7 characters, then 6, ...., then 1 character
    length = 7
    while length > 0:
        short = book_name[0:length].upper()
        for idx in range(len(book_names)):
            if book_names[idx][0:length].upper().find(short) >= 0:
                return idx
        # prepare for next loop
        length = length - 1

    return -1

# book_name ==> get list of 20 books that are before book_name and
# 20 books that are after book_name
def get_books_close_by_in_name(book_name):
    idx = get_first_index_closes_to_name(book_name)
    print(f"idx for {book_name} = ",idx)
    the_list = []
    if idx < 0:
        return the_list
    
    lower = idx - int(max_books_to_display/2)
    if lower < 0:
        lower = 0
    higher = idx + int(max_books_to_display/2)
    if higher >= num_books_in_list:
        higher = num_books_in_list - 1
    for i in range(lower,higher):
        the_list.append((book_names[i],0.00))

    return the_list


@app.route("/")
def home():
    return "Hello! there! <h1>HEY-HEY 210626 0118pm</h1>"


@app.route("/admin")
def admin():
    return redirect(url_for("user",name="Admin!"))


@app.route("/get_books",methods=["POST","GET"])
def login():
    if request.method == "POST":
        print(f"in 'def login', method = POST, name={request.form['nm']}")
    else:
        print("in 'def login', method = GET")

    if request.method == "POST":
        bookname = request.form['nm']
        the_list = get_ordered_list_for_book(bookname)
        session['show_full_book_title'] = 0
        
        if len(the_list) <= 0:
            the_list = get_books_close_by_in_name(bookname)
            session['show_full_book_title'] = 1
        
        the_list = the_list[0:max_books_to_display]
        session['sim_books'] = the_list
        return redirect(url_for("user",name=bookname))
    else:
        return render_template("GetBookName.html")

@app.route("/<name>")
def user(name):
    the_book_list = "";
    display_full_title = False
    if 'show_full_book_title' in session:
        if session['show_full_book_title'] == 1:
            display_full_title = True
        
    if 'sim_books' in session:
        
        the_book_list = "\
<head> \
<style> \
table { \
  font-family: arial, sans-serif; \
  border-collapse: collapse; \
  width: 100%; \
} \
\
td, th { \
  border: 1px solid #dddddd; \
  text-align: left; \
  padding: 8px; \
} \
\
tr:nth-child(even) { \
  background-color: #dddddd; \
}\
</style> \
</head>\
<table>\
<tr> \
<th>Book Name</th> \
<th>Close-ness Factor</th> \
</tr>"

        
        bk_list_len = len(session['sim_books'])
        if bk_list_len > 0:
            num_to_display = bk_list_len
            if num_to_display > max_books_to_display:
                num_to_display = max_books_to_display
            for i in range(num_to_display):
                if session['sim_books'][i][0] != name:
                    book,correlation = session['sim_books'][i]
                    if display_full_title == False:
                        the_book_list = the_book_list + f"<tr><td>{book[0:60].ljust(60)}</td> <td>{correlation:.3f}</td></tr>"
                    else:
                        the_book_list = the_book_list + f"<tr><td>{book}</td> <td>Close-by in Name Only</td></tr>"
            the_book_list = the_book_list + "</table>"            

            if display_full_title == False:
                return f"<h1> Books that are similar to '{name}'</h1>" + the_book_list
            else:
                return f"<h1> Books that are close-by in name only to '{name}'</h1>" + the_book_list

if __name__ == "__main__":
    app.run(port=5000,host="0.0.0.0",debug=True)






