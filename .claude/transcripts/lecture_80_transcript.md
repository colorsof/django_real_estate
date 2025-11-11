Before you can continue focusing on the front end.

I upgraded my version of Docker.

So if I say docker dash dash version and so the Docker version I'm currently using is now 26.

And when you build your containers now you're going to see this warning.

Let me show you up above here.

You're going to be told, uh, that uh, version is now obsolete in this new version of Docker.

So what you need to do is my containers are running, so I just bring them down with make down.

And then let's go back to our compose file.

So in API a local imnl let's get rid of this version line.

That is the new recommended change because of this update to Docker.

Then you save that.

Now that we've removed the version line because it's no longer required as of Docker version 25.

Now let's go back to our terminal.

Then let's run make a build.

This time you see there is no warning and things should still work.

Good or containers have been studied and there is no warning.

So let's go back to our browser and confirm that our basic Next.js front end is still working.

Let's reload.

Good.

The home page is working.

Then if you go to Docker Desktop, you're going to see that our containers are running.

So because technology keeps on changing now there's a new version of Docker and some things are breaking.

So as the changes are going to be happening, I'm going to be updating the course and making the necessary

corrections.

And so far we have a basic Next.js front end setup.

Let's continue with this.

So we shall first configure our Linters and code Formatters.

That is ESLint and prettier.

Prettier is a code formatter that focuses on code formatting and style consistency.

It automatically formats your code as per a predefined set of rules.

ESLint, on the other hand, is a linter that allows you to define custom linting rules and enforces

coding standards.

It helps you identify and fix potential errors and enforces consistent coding styles.

Also, in a terminal, make sure you're in the client directory now.

So let's make sure we CD into client.

And then let's install some packages as dev dependencies.

So you can say npm install dash d.

We're going to install eslint config standard which is this version 17 .1.0.

Then eslint plugin tailwind CSS version three point 14.1, then eslint config a prettier version 9.1.0,

then prettier 3.2.4 and a sharp 0.33.2.

So let me install this and explain.

So ESLint standard config basically provides eslint configuration over the JavaScript standard style

and eslint plugin.

Tailwind CSS enforces best practices while using tailwind CSS, such as organizing tailwind CSS class

names and making them easier to read and review.

Then this ESLint config prettier basically turns off all rules that are unnecessary or might conflict

with prettier when using prettier with ESLint and prettier.

Here is our code formatter and sharp is a high speed node API module, which is used to convert large

images in common formats into smaller versions which are more web friendly, such as JPEG, PNG, etc.

and then we are told there's a new minor version of npm available and we need to upgrade it.

And so what we run is npm install dash g, then npm at 10.7 0.0.

Good.

So once that is updated, then we can also install an icon pack that you're going to be using.

So you can run npm install.

Then add a hero icons react.

Make sure you're still in the client directory.

Good.

Then after the installation is done, let's first set up prettier.

Let's go back to your IDE.

Then in the root of the client directory, which is at the same level as the package.json file, we're

going to create a dot prettier rc file.

So you can right click here.

New file.

It's dot prettier like that.

Then RC.

Then we're going to configure some settings for prettier.

So we can first start with the tab width.

So for the tab width I'm going to leave minus two.

And then my print width.

My print width is going to be 80.

And then I'm going to use tabs.

So say use tabs.

We're going to set that to true.

And then double quotes.

We're going to set that to true.

Then this is not supposed to be double quotes.

It's supposed to be double quotes like that.

Then you save that file.

If you're using VS code, make sure you have the ESLint and Preeti extensions installed.

So as you can see I have them installed.

So es lint I have it installed and then I have prettier installed too.

So let me search for prettier in my extensions.

Good, I have it installed.

Then back in the client directory we have this dot eslint rc JSON file.

So open it.

It was automatically created by Next.js.

Now we're going to make some changes to account for the plugins that we installed.

Remember the plugins installed in our terminal which were these.

And so we want to set these ones up.

So go back to ESLint RC.

And then we're going to add a setting here for ignore.

As you can see ignore patterns.

And that's going to be an array.

And we're going to say src slash components a slash UI.

Then slash star star double star like that in the extends.

Now this is going to change to a list because we're going to have many configurations.

So change that into an array.

The first one is going to be next core web vitals.

And then we're going to add standard then plugin.

Now full colon a tailwind CSS.

And so tailwind CSS a slash recommended.

And then we're going to have prettier like that.

Then after extends we're going to set up some rules.

So you can say rules here.

And so these rules the first one is going to be camel case.

So camel case we're going to set that to off.

And then no unused variables.

So no hyphen unused vars.

So we're going to set that to off.

And then our tailwind CSS.

So tailwind CSS then slash no hyphen custom class name.

We're going to set that to off.

And that's it for this ESLint dot rc JSON file.

Now that you're done configuring prettier and ESLint.

As I mentioned before, I'm going to be using a shared UI for my UI components.

A shared CDN UI is basically a collection of reusable components that you can copy and paste into your

applications, meaning it's not a dependency that needs to be installed, but rather you're going to

pick the components you need and add them to your project and customize them to your needs.

The approach that Shad CDN takes makes it much smaller and lightweight, unlike other UI libraries,

which force you to install everything.

That's why I like Shad Khan.

And so to start off with Shad Khan UI, we're going to initialize the shared CDN using its CLI.

And so go back to your terminal.

Then make sure you're still in the clients directory.

As you see we're in client.

Then we're going to now say Npx Richardson hyphen UI add latest then initialize.

Then we're going to be asked some questions.

So which style would you like to use.

Let's just select default and then the base color just select on slate then CSS variables select yes.

Then let's shut CDN do its thing.

Good.

The Schudson project has been initialized.

Now we may add components.

So what you're going to realize is if you go back to your clients directory in the clients root are

components to the JSON file is going to be created, as you can see, which is this.

And this components or JSON file is going to be created with the choices that we selected when we were

initializing Shadchan UI.

And then also some additional packages have been installed in the package.json file.

So if you go to package.json you're going to see some dependencies have also been installed.

And so within S.A.C. click on it.

You're going to see.

Now we have a components directory and a lib directory.

The components directory is going to be empty for now since we haven't added any shadchan components.

But for the lib folder it has some utils and these utilities are related to shadchan.

Then if we check in the global CSS file in src app, then global CSS.

A shared CDN has added some CSS variables, so feel free to delete all of them such that the file remains

like before.

As you can see here.

Added all these.

So what we're going to do is we're just going to delete everything.

Like that.

Then you save the file.

All that you want left is at Tailwind base, Tailwind components and at Tailwind Utilities.

Then you save that file.

So make sure you make that correction.

And then we're also going to amend the tailwind config file to remove the colors and the border radius

that Schudson added.

And so if you go to a client then open a tailwind config dot ts.

And so within tailwind config dot ts we're going to remove the colors and the border radius.

And so let's see uh that is okay.

This is okay.

Then let's go to the extent object which is this.

So what we're going to remove is these colors.

So on colors we're going to make this empty.

So get rid of all these colors that are created.

Just make colors an empty object.

And just like that, after removing everything from colors, we're going to add border radius.

So say border radius like that, then make it an empty object.

Then you can leave keyframes as it is.

Then animation is okay.

Then for the plugins we're going to require tailwind CSS animate which is okay.

Then satisfies config.

This is okay and this is okay.

And so that's it for our tailwind config dot ts.

Then before building our containers let's configure Next.js to be aware of the images from our remote

host which is going to be Cloudinary.

This ensures that only external images from our Cloudinary account can be served from the Next.js Image

Optimization API.

So you go back to your Next.js config which is in client, then Next.js config.

So just open that.

So it sees Next.js config dot mjs.

Then what you're going to do is within next config.

Here we can now say our images like that.

We're going to add our remote patterns.

So you can say remote patterns.

And the remote patterns you want to add is our host name.

And we can now say host name here.

This is a cloudinary.

So you can say in quotation marks res.cloudinary.com like that.

And then you save that file.

Then once you've set the host name you can save the file.

Then remember.

And since we've added new packages we have to bring our containers down and rebuild them again.

Because remember packages are installed in our containers at build time and not runtime.

So go back to your terminal.

Then let's CD out of client.

Now we're in our root directory.

If you can confirm that is at the same location as the local ML, then now we can say make down.

Good.

Then make.

Build.

Good.

Once the containers are built, let's go back to our browser and reload our home page to see if everything

works well.

So reload this.

Good.

We're now going to see that our home page is running, and you can confirm from the Docker desktop that

all our containers are up and running.

Remember you can also do the same on Portainer.

So just click on Portainer.

And so once Portainer has loaded you can just click on home then click on that, then containers and

you're going to see all our containers are running.

And since everything is working well and our default home page is still working, let's go back to our

git client.

And you can make a commit.

So you can see this one is actual.

And this one was basically set up a shared CDN UI, then prettier and eslint like that.

And then you can make the commit.

And that's it for this lecture.

I'll see you in the next lecture where we're going to be setting up our phones.


