1. Import `Optional` from `typing`(Python standard module) to declare fields that could be `None`.

2. Import `connect` and `Document` from `mongodb_odm`. `connect` function will be used to set connection with database. Use `Document` class as a parent class of our database models.

3. Create the `Player` model class, representing the `player` collection in the database.

4. Create the `name` field. The field was a required, so there's no default value, and it's not Optional.

5. The `country_code` field will behave as an plain `string` field as like `name`

6. Create the `rating` nullable int field. In the database, the default value will be `null`, the python equivalent of `None`. As this field could be `None` (and `null` in the database), we declare it with `Optional[int]`.

7. There's a single `main()` function now that contains all the code that should be executed when running the program from the console. So this is all we need to have in the main block. Just call the `main()` function.

8. We have a `main()` function with all the code that should be executed when the program is called as a script from the console. That way we can add more code later to this function.We then put this function `main()` in the main block below. As it is a single function, other Python files could import it and call it directly.

9. We set connection with our database by passing connection string in the function `connect` that import from `mongodb_odm`.

10. And now we are also creating the players in this `main()` function.

11. Here we create all `Player` compact in a function for better understandability.

12. We created our first object. Create the data in database by calling `create()` method.

13. We declare second `Player` object. We did not save/create data in the database instantly.

14. We save all data to database by calling `create()` method of `maradona` object that are previously defined.