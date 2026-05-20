# Initial Thoughts, Plans, Description, etc.

## Different Approaches

### Criteria

- Price - Higher Score = Less Price - Weighting(Depends bc if it's really expensive it's really low, but it doesn't matter that much since fallout)
- Accuracy - Very Important
- Time - Sweet spot of 30 Hours(although all these options can be less or more depending on how big you wanna go on the software side)
- Difficulty - Sweet spot of 5-7/10 = 9/10(confusing ik)

- Magnetic Sensors
  - Summary: So the idea is that you have indivual magnetic sensors below each of 64 squares. The downside about this is that technically you can't tell what piece is which. However, you can guess pretty well based on the last game state. That is probably why I will need a 2 key switchs + OLED to communicate with the user if the board is set up or not, game updates, etc.
  - Ratings
    - Price - 6/10
    - Accuracy - 9/10
    - Time - 9/10
    - 6-7/10 - (so 8.5/10)
- CV
  - Summary: So the idea is that there is a camera of some sorts above the board(or any angle technically) that sees pieces. The problem of this is that it is inconvienient as they need to set up a camera and it might not be as accurate
  - Ratings
    - Price - 10/10
    - Accuracy - 7.5/10
    - Time - 8/10
    - 4/10 so 6/10
  
## Verdict

Obviously magnetic sensors.

Let us just figure out what stuff is needed and what it will cost :O

- Reed Switch Magentic Switch - [2x14mm MKA14103 for 0.73/5 pieces](https://www.aliexpress.us/item/3256801651270926.html?spm=a2g0o.productlist.main.27.1b353509EnCkGa&utparam-url=scene%3Asearch%7Cquery_from%3Apc_back_same_best%7Cx_object_id%3A1005001837585678%7C_p_origin_prod%3A&algo_pvid=153569b3-7627-4b91-ae5d-54dbf97488d1&algo_exp_id=153569b3-7627-4b91-ae5d-54dbf97488d1&pdp_ext_f=%7B%22order%22%3A%22330%22%2C%22fromPage%22%3A%22search%22%7D&pdp_npi=6%40dis%21USD%211.39%210.99%21%21%211.39%210.99%21%402103212517770669853511261eb7b2%2112000017803497619%21sea%21US%213107961229%21ABX%211%210%21n_tag%3A-29910%3Bd%3A4414e135%3Bm03_new_user%3A-29895%3BpisId%3A5000000204886261&gatewayAdapt=4itemAdapt) - getting 70 bc packaging is bad so total price + shipping - about $15
- With 8 rows & Columns using key matricies
- 2 keys
- A nob
- and 1 inch oleds