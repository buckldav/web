---
title: FARP Stack - 4. React Admin
description: Create a dashboard with React Admin.
---

## Introduction

There are lots of opinions and ways to make frontends for web applications. Of course, it's paramount that one has a little understanding of HTML, CSS, and JavaScript, the backbone of the web. To enable easier development for large applications, a lot of teams turn to libraries and frameworks to help assist in the development of structure and functionality.

## React

React is a mature, popular framework that's over a decade old. While many libraries and frameworks have come before and since, React has stood the test of time and has one of the largest ecosystems out there. Here are some brief examples of how it works (taken from [https://react.dev](react.dev)):

### Component-Driven Design

Create your own custom elements called "components." You can specify custom attributes (known as props) and use them modularly in your app.

```jsx
function Video({ video }) {
  return (
    <div>
      <Thumbnail video={video} />
      <a href={video.url}>
        <h3>{video.title}</h3>
        <p>{video.description}</p>
      </a>
      <LikeButton video={video} />
    </div>
  );
}
```

### JSX

React's custom syntax is called JSX, where every component is a JavaScript function that returns transpiled HTML, CSS, and JS, all bundled together.

```jsx
function VideoList({ videos, emptyHeading }) {
  const count = videos.length;
  let heading = emptyHeading;
  if (count > 0) {
    const noun = count > 1 ? 'Videos' : 'Video';
    heading = count + ' ' + noun;
  }
  return (
    <section>
      <h2>{heading}</h2>
      {videos.map(video =>
        <Video key={video.id} video={video} />
      )}
    </section>
  );
}
```

### Manage State

Components can be stateful, they can both keep track of data and logic, and manage how that data is displayed and interacted with.

```jsx
import { useState } from 'react';

function SearchableVideoList({ videos }) {
  const [searchText, setSearchText] = useState('');
  const foundVideos = filterVideos(videos, searchText);
  return (
    <>
      <SearchInput
        value={searchText}
        onChange={newText => setSearchText(newText)} />
      <VideoList
        videos={foundVideos}
        emptyHeading={`No matches for “${searchText}”`} />
    </>
  );
}
```

## React Admin

React Admin is a React-driven framework that is optimized for CRUD application dashboards, where user interfaces are built to show, create, edit, and delete data.

Simply follow the tutorial at [https://marmelab.com/react-admin/Tutorial.html](https://marmelab.com/react-admin/Tutorial.html). In this lesson, you won't need to worry about a backend, you can connect your app to a fake data API. Wherever it says `npm`, we recommend using `pnpm`. The commands are the same. 

In the next lesson, you will create a React Admin frontend for your existing API.
