### directory used by frontend by now

![image-20210805010450631](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210805010450631.png)

![image-20210805010505878](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210805010505878.png)

in setting.py:

![image-20210805010701978](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210805010701978.png)

All the .css used are in "css file".All the images are downloaded from Unsplash, whose photos are free for business use, so no copyright problems.

![image-20210806022758956](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210806022758956.png)

The pages from me will be like this. Actually it is all the page that needed in current Himanshu's code. So if all of this works well the functions would look beautiful.

## What pages look like?

### login page:

![image-20210805013941476](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210805013941476.png)

signin.css added in **css** folder.

picture of Bolt in **image** folder.

(Failed to upload a bg img)

```
.bg{  
background:url(http://wyz.67ge.com/wp-content/uploads/qzlogo.jpg);  
filter:"progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod='scale')";  
-moz-background-size:100% 100%;  
    background-size:100% 100%;  
}
```

#### Things need to do:

make it work in Bolt-main, the project. There's example in the book Chepter12.

<u>unsolved</u>

facebook twitter



### Index page:

![index01](C:\Users\Administrator\Downloads\IT\IT project\images downloaded\index01.JPG)

It is a carousel. That is, the page will automatically move. Those three pages in carousel will link to "About us" "Shelter" "Register". It is like ads.

![index02](C:\Users\Administrator\Downloads\IT\IT project\images downloaded\index02.JPG)



![index03](C:\Users\Administrator\Downloads\IT\IT project\images downloaded\index03.JPG)

It is just normal introducing content. 

![index04](C:\Users\Administrator\Downloads\IT\IT project\images downloaded\index04.JPG)

#### Things need to do:

add "Shelter" and "Add Shelter" in the top nav bar.



About me :

![about01](C:\Users\Administrator\Downloads\IT\IT project\images downloaded\about01.JPG)

the top

![about02](C:\Users\Administrator\Downloads\IT\IT project\images downloaded\about02.JPG)

the middle

![about03](C:\Users\Administrator\Downloads\IT\IT project\images downloaded\about03.JPG)

the bottom

### Shelter:

![shelter01](C:\Users\Administrator\Downloads\IT\IT project\images downloaded\shelter01.JPG)

There's a button: Add an animal here. (Add Shelter is in index page)

![shelter02](C:\Users\Administrator\Downloads\IT\IT project\images downloaded\shelter02.JPG)



**Register** is the same as login. I'll go fast to Chapter 12 to handle it.

![image-20210806024637589](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20210806024637589.png)

In Bolt it should be more complicated because there's user photo that should be uploaded.



As for **Add animal** and **Add Shelter**, they both concerns to a challenge, that is creating place for user to upload pictures and receive. And some operation concerning to database. I'll try to make that page looks good. If I can handle the core logic, then the two pages can be settled since they are alike.

## Things to do now:

1. I didn't **extend** the pages from a base.html. But there is surely something repeated in the code. like <head> , that top navigate bar. However, there is  change in different pages in header. I don't know whether the link can go in to <main> part or <body> part.
2. so create a base.html and edit all the pages' code
3. merge the code in Himanshu's code
4. Go through chapter 9 to 12, handle login, register, add_animal, add_shelter.
5. In shelter page, if a new animal is added, the "displaying card" will be added. It's a dynamic page. Solve it.
6. Upload the code in repo, but in new directory, so that the current code won't be influenced.







*some of my own note. (just ignore)

https://laracasts.com/discuss/channels/laravel/images-not-loading-on-server-404-error

这里有if else 的写法

```html
<img class="bd-placeholder-img" width="200" height="250" src="static/images/aboutpic04.jpg"  preserveAspectRatio="xMidYMid slice" focusable="false">
```

存图的好写法

