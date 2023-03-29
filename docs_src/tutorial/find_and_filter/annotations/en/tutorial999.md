1. Import `Optional` from `typing`(Python standard module) to declare fields that could be `None`.

2. Import all the necessary function and class from `mongodb_odm`

3. Create the `Player` model class, representing the `player` collection in the database.

4. Create the `name` field. The field was a required, so there's no default value, and it's not Optional.

5. The `country_code` field will behave as an plain `string` field as like `name`

6. Create the `rating` nullable int field. In the database, the default value will be `null`, the python equivalent of `None`. As this field could be `None` (and `null` in the database), we declare it with `Optional[int]`.

7. Define `Config` class to change certain behavior for `Player` class.

8. Create a index for `country_code` field with the help of `IndexModel` imported from `Pymongo`

9. There's a single `main()` function now that contains all the code that should be executed when running the program from the console. So this is all we need to have in the main block. Just call the `main()` function.

10. We have a `main()` function with all the code that should be executed when the program is called as a script from the console. That way we can add more code later to this function.We then put this function `main()` in the main block below. As it is a single function, other Python files could import it and call it directly.

11. We set connection with our database by passing connection string in the function `connect` that import from `mongodb_odm`.

12. With calling `apply_indexes()` all indexes will be created in database.

13. And now we are also creating the players in this `main()` function.

14. Here we create all `Player` compact in a function for better understandability.

15. Here we call `read_players` function to check read functionality.

16. Here we read all `Player` data compact in a function for better understandability.

17. By calling find function of `Player` class. The player data should pull from database. Return data will be a iterator. Return data was not an list. So we are not able to access the data by index like `players[0]`(Will raise error).

18. Here we iterate over `players`. The loop will be automatically terminate when iterator was end as default behavior of a iterator.

19. Here we call `filter_players` function to check filter functionality.

20. In this function we will filter out all the player and will understand how filter work in `mongodb_odm`.

21. Here we filter out all the player which has total employee getter than or equal to `10`. We can use `find` method for both **read** and **filter**. This is same method but receive multiple optional parameter. Find method return iterator. It's iterable but not accessible like `list[0]`.

22. Here we iterate over `players` that has total employee getter than or equal to `10`. All will be work on `players` variable that are support by iterator. We can use `next(players)`.

23. 23

24. 24

25. 25

26. 26

27. 27

28. 28

29. 29

30. 30

31. 31

32. 32

33. 33

34. 34

35. 35

36. 36

37. 37

38. 38

39. 39

40. 40

41. 41

42. 42

43. 43

44. 44

45. 45
