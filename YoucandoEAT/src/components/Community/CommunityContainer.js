import React, { useState } from "react";
import CommunityPresenter from "./CommunityPresenter";
import Dummy from "../../assets/권은비2.jpg";

function CommunityContainer() {
  const [posts, setPosts] = useState([
    {
      title: "Dummy Title1",
      content: "dummy content",
      date: "2021-04-18 21:52",
      writer: "Lena",
      thumbnail: Dummy,
    },

    {
      title: "Dummy Title2",
      content: "dummy content",
      date: "2021-04-18 21:52",
      writer: "Lena",
      thumbnail: Dummy,
    },

    {
      title: "Dummy Title3",
      content: "dummy content",
      date: "2021-04-18 21:52",
      writer: "Lena",
      thumbnail: Dummy,
    },

    {
      title: "Dummy Title4",
      content: "dummy content",
      date: "2021-04-18 21:52",
      writer: "Lena",
      thumbnail: Dummy,
    },

    {
      title: "Dummy Title5",
      content: "dummy content",
      date: "2021-04-18 21:52",
      writer: "Lena",
      thumbnail: Dummy,
    },

    {
      title: "Dummy Title6",
      content: "dummy content",
      date: "2021-04-18 21:52",
      writer: "Lena",
      thumbnail: Dummy,
    },

    {
      title: "Dummy Title7",
      content: "dummy content",
      date: "2021-04-18 21:52",
      writer: "Lena",
      thumbnail: Dummy,
    },

    {
      title: "Dummy Title8",
      content: "dummy content",
      date: "2021-04-18 21:52",
      writer: "Lena",
      thumbnail: Dummy,
    },

    {
      title: "Dummy Title9",
      content: "dummy content",
      date: "2021-04-18 21:52",
      writer: "Lena",
      thumbnail: Dummy,
    },
  ]);

  console.log(posts);

  return (
    <>
      <CommunityPresenter posts={posts} />
    </>
  );
}

export default CommunityContainer;