from cat_class import Cats

cat_list = [Cats(name="Baron", sex="Male", age=2),
            Cats(name="Sam", sex="Male", age=2)]

for cats in cat_list:
    cats.print_cats()
