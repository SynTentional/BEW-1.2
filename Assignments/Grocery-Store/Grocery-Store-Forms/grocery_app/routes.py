from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem
# from grocery_app.forms import BookForm, AuthorForm, GenreForm

# Import app and db from events_app package so that we can run app
from grocery_app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    # TODO: Create a GroceryStoreForm

    # TODO: If form was submitted and was valid:
    # - create a new GroceryStore object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the store detail page.

    # TODO: Send the form to the template and use it to render the form fields
   form = GroceryStoreForm()

    if form.validate_on_submit():
      new_store = GroceryStore(
        title = form.title.data,
        address = form.address.data,
        created_by = current_user,
      )
      db.session.add(new_store)
      db.session.commit()

      flash("New store was created successfully")
      return redirect(url_for('main.store_detail', store_id=new_store.id))

    return render_template('new_store.html', form=form)


@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    # TODO: Create a GroceryItemForm

    # TODO: If form was submitted and was valid:
    # - create a new GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.

    # TODO: Send the form to the template and use it to render the form fields
    form = GroceryItemForm()
    
    if form.validate_on_submit():
      new_item = GroceryItem(
        name = form.name.data,
        price = form.price.data,
        category = form.category.data,
        photo_url = form.photo_url.data,
        store = form.store.data,
        created_by = current_user,
      )
      db.session.add(new_item)
      db.session.commit()

      flash("New item was created successfully")
      return redirect(url_for('main.item_detail', item_id=new_item.id))

    return render_template('new_item.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    # TODO: Create a GroceryStoreForm and pass in `obj=store`

    # TODO: If form was submitted and was valid:
    # - update the GroceryStore object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the store detail page.

    # TODO: Send the form to the template and use it to render the form fields
    store = GroceryStore.query.get(store_id)

    form = GroceryStoreForm(obj=store)

    if form.validate_on_submit():
      store.query.filter_by(id=store_id)
      store.name = form.name.data
      store.address = form.address.data
      store.items = form.items.data

      db.session.add(store)
      db.session.commit()

    return render_template('store_detail.html', store=store, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    # TODO: Create a GroceryItemForm and pass in `obj=item`

    # TODO: If form was submitted and was valid:
    # - update the GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.

    # TODO: Send the form to the template and use it to render the form fields
    item = GroceryItem.query.get(item_id)
    form = GroceryItemForm(obj=item)

    if form.validate_on_submit():
      item.query.filter_by(id=item_id)
      item.name = form.name.data
      item.price = form.price.data
      item.category = form.category.data
      item.photo_url = form.photo_url.data
      item.store = form.store.data

      db.session.add(item)
      db.session.commit()

    return render_template('item_detail.html', item=item, form=form)


###########################
#        Auth Routes      #
###########################

auth = Blueprint("auth", __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))
