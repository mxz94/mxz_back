import Fuse from "fuse.js";
import React, { useEffect, useRef, useState, useMemo } from "react";
import Card from "@components/Card";
import slugify from "@utils/slugify";
import type { CollectionEntry } from "astro:content";

export type SearchItem = {
  title: string;
  description: string;
  data: CollectionEntry<"blog">["data"];
};

interface Props {
  searchList: SearchItem[];
}

interface SearchResult {
  item: SearchItem;
  refIndex: number;
}
import algoliasearch from "algoliasearch/lite";
import {
  Configure,
  Highlight,
  Hits,
  InstantSearch,
  RefinementList,
  SearchBox,
} from "react-instantsearch";
import CustomSearchBox from "@components/CustomSearchBox.tsx";

const searchClient = algoliasearch(
  "QP4WN0IB1W",
  "08b36ae83999b4ea83345429017ca3ba"
);

function Hit({ hit }) {
  var url = "https://mxz-back.pages.dev/posts/" + hit.url;
  return (
    <article>
      <a href={url}>
        <h1 className={"th1"}>
          <Highlight attribute="title" hit={hit} />
        </h1>
        <p className={"cp"}>
          <Highlight attribute="content" hit={hit} />
        </p>
      </a>
    </article>
  );
}

export default function SearchBar2({ searchList }: Props) {
  return (
    <InstantSearch searchClient={searchClient} indexName="dev_blog">
      <CustomSearchBox></CustomSearchBox>
      <Hits hitComponent={Hit} />
    </InstantSearch>
  );
}
