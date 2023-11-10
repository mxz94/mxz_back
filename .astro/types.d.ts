declare module 'astro:content' {
	interface Render {
		'.md': Promise<{
			Content: import('astro').MarkdownInstance<{}>['Content'];
			headings: import('astro').MarkdownHeading[];
			remarkPluginFrontmatter: Record<string, any>;
		}>;
	}
}

declare module 'astro:content' {
	export { z } from 'astro/zod';

	type Flatten<T> = T extends { [K: string]: infer U } ? U : never;

	export type CollectionKey = keyof AnyEntryMap;
	export type CollectionEntry<C extends CollectionKey> = Flatten<AnyEntryMap[C]>;

	export type ContentCollectionKey = keyof ContentEntryMap;
	export type DataCollectionKey = keyof DataEntryMap;

	// This needs to be in sync with ImageMetadata
	export type ImageFunction = () => import('astro/zod').ZodObject<{
		src: import('astro/zod').ZodString;
		width: import('astro/zod').ZodNumber;
		height: import('astro/zod').ZodNumber;
		format: import('astro/zod').ZodUnion<
			[
				import('astro/zod').ZodLiteral<'png'>,
				import('astro/zod').ZodLiteral<'jpg'>,
				import('astro/zod').ZodLiteral<'jpeg'>,
				import('astro/zod').ZodLiteral<'tiff'>,
				import('astro/zod').ZodLiteral<'webp'>,
				import('astro/zod').ZodLiteral<'gif'>,
				import('astro/zod').ZodLiteral<'svg'>,
				import('astro/zod').ZodLiteral<'avif'>,
			]
		>;
	}>;

	type BaseSchemaWithoutEffects =
		| import('astro/zod').AnyZodObject
		| import('astro/zod').ZodUnion<[BaseSchemaWithoutEffects, ...BaseSchemaWithoutEffects[]]>
		| import('astro/zod').ZodDiscriminatedUnion<string, import('astro/zod').AnyZodObject[]>
		| import('astro/zod').ZodIntersection<BaseSchemaWithoutEffects, BaseSchemaWithoutEffects>;

	type BaseSchema =
		| BaseSchemaWithoutEffects
		| import('astro/zod').ZodEffects<BaseSchemaWithoutEffects>;

	export type SchemaContext = { image: ImageFunction };

	type DataCollectionConfig<S extends BaseSchema> = {
		type: 'data';
		schema?: S | ((context: SchemaContext) => S);
	};

	type ContentCollectionConfig<S extends BaseSchema> = {
		type?: 'content';
		schema?: S | ((context: SchemaContext) => S);
	};

	type CollectionConfig<S> = ContentCollectionConfig<S> | DataCollectionConfig<S>;

	export function defineCollection<S extends BaseSchema>(
		input: CollectionConfig<S>
	): CollectionConfig<S>;

	type AllValuesOf<T> = T extends any ? T[keyof T] : never;
	type ValidContentEntrySlug<C extends keyof ContentEntryMap> = AllValuesOf<
		ContentEntryMap[C]
	>['slug'];

	export function getEntryBySlug<
		C extends keyof ContentEntryMap,
		E extends ValidContentEntrySlug<C> | (string & {}),
	>(
		collection: C,
		// Note that this has to accept a regular string too, for SSR
		entrySlug: E
	): E extends ValidContentEntrySlug<C>
		? Promise<CollectionEntry<C>>
		: Promise<CollectionEntry<C> | undefined>;

	export function getDataEntryById<C extends keyof DataEntryMap, E extends keyof DataEntryMap[C]>(
		collection: C,
		entryId: E
	): Promise<CollectionEntry<C>>;

	export function getCollection<C extends keyof AnyEntryMap, E extends CollectionEntry<C>>(
		collection: C,
		filter?: (entry: CollectionEntry<C>) => entry is E
	): Promise<E[]>;
	export function getCollection<C extends keyof AnyEntryMap>(
		collection: C,
		filter?: (entry: CollectionEntry<C>) => unknown
	): Promise<CollectionEntry<C>[]>;

	export function getEntry<
		C extends keyof ContentEntryMap,
		E extends ValidContentEntrySlug<C> | (string & {}),
	>(entry: {
		collection: C;
		slug: E;
	}): E extends ValidContentEntrySlug<C>
		? Promise<CollectionEntry<C>>
		: Promise<CollectionEntry<C> | undefined>;
	export function getEntry<
		C extends keyof DataEntryMap,
		E extends keyof DataEntryMap[C] | (string & {}),
	>(entry: {
		collection: C;
		id: E;
	}): E extends keyof DataEntryMap[C]
		? Promise<DataEntryMap[C][E]>
		: Promise<CollectionEntry<C> | undefined>;
	export function getEntry<
		C extends keyof ContentEntryMap,
		E extends ValidContentEntrySlug<C> | (string & {}),
	>(
		collection: C,
		slug: E
	): E extends ValidContentEntrySlug<C>
		? Promise<CollectionEntry<C>>
		: Promise<CollectionEntry<C> | undefined>;
	export function getEntry<
		C extends keyof DataEntryMap,
		E extends keyof DataEntryMap[C] | (string & {}),
	>(
		collection: C,
		id: E
	): E extends keyof DataEntryMap[C]
		? Promise<DataEntryMap[C][E]>
		: Promise<CollectionEntry<C> | undefined>;

	/** Resolve an array of entry references from the same collection */
	export function getEntries<C extends keyof ContentEntryMap>(
		entries: {
			collection: C;
			slug: ValidContentEntrySlug<C>;
		}[]
	): Promise<CollectionEntry<C>[]>;
	export function getEntries<C extends keyof DataEntryMap>(
		entries: {
			collection: C;
			id: keyof DataEntryMap[C];
		}[]
	): Promise<CollectionEntry<C>[]>;

	export function reference<C extends keyof AnyEntryMap>(
		collection: C
	): import('astro/zod').ZodEffects<
		import('astro/zod').ZodString,
		C extends keyof ContentEntryMap
			? {
					collection: C;
					slug: ValidContentEntrySlug<C>;
			  }
			: {
					collection: C;
					id: keyof DataEntryMap[C];
			  }
	>;
	// Allow generic `string` to avoid excessive type errors in the config
	// if `dev` is not running to update as you edit.
	// Invalid collection names will be caught at build time.
	export function reference<C extends string>(
		collection: C
	): import('astro/zod').ZodEffects<import('astro/zod').ZodString, never>;

	type ReturnTypeOrOriginal<T> = T extends (...args: any[]) => infer R ? R : T;
	type InferEntrySchema<C extends keyof AnyEntryMap> = import('astro/zod').infer<
		ReturnTypeOrOriginal<Required<ContentConfig['collections'][C]>['schema']>
	>;

	type ContentEntryMap = {
		"blog": {
"2010/2010-10-01(6年前写的).md": {
	id: "2010/2010-10-01(6年前写的).md";
  slug: "2010/2010-10-016年前写的";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2010/2010-10-01(小计).md": {
	id: "2010/2010-10-01(小计).md";
  slug: "2010/2010-10-01小计";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2010/2010-10-01(房东们).md": {
	id: "2010/2010-10-01(房东们).md";
  slug: "2010/2010-10-01房东们";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2010/2010-10-01(狗).md": {
	id: "2010/2010-10-01(狗).md";
  slug: "2010/2010-10-01狗";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-10(记录第一天).md": {
	id: "2020/2020-10-10(记录第一天).md";
  slug: "2020/2020-10-10记录第一天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-11（节后带饭）.md": {
	id: "2020/2020-10-11（节后带饭）.md";
  slug: "2020/2020-10-11节后带饭";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-12(划水第二天).md": {
	id: "2020/2020-10-12(划水第二天).md";
  slug: "2020/2020-10-12划水第二天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-13-微风细雨.md": {
	id: "2020/2020-10-13-微风细雨.md";
  slug: "2020/2020-10-13-微风细雨";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-14(以为今天是星期四).md": {
	id: "2020/2020-10-14(以为今天是星期四).md";
  slug: "2020/2020-10-14以为今天是星期四";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-15(下班吃枣回家).md": {
	id: "2020/2020-10-15(下班吃枣回家).md";
  slug: "2020/2020-10-15下班吃枣回家";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-16(周五，休息).md": {
	id: "2020/2020-10-16(周五，休息).md";
  slug: "2020/2020-10-16周五休息";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-17（忙碌逛街做饭的周末）.md": {
	id: "2020/2020-10-17（忙碌逛街做饭的周末）.md";
  slug: "2020/2020-10-17忙碌逛街做饭的周末";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-18（惬意周末）.md": {
	id: "2020/2020-10-18（惬意周末）.md";
  slug: "2020/2020-10-18惬意周末";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-19(志超太有趣了).md": {
	id: "2020/2020-10-19(志超太有趣了).md";
  slug: "2020/2020-10-19志超太有趣了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-20(我哥又来深圳了，阿范来接我).md": {
	id: "2020/2020-10-20(我哥又来深圳了，阿范来接我).md";
  slug: "2020/2020-10-20我哥又来深圳了阿范来接我";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-21（狗范暴躁的一天）.md": {
	id: "2020/2020-10-21（狗范暴躁的一天）.md";
  slug: "2020/2020-10-21狗范暴躁的一天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-22（充满爱意的早上）.md": {
	id: "2020/2020-10-22（充满爱意的早上）.md";
  slug: "2020/2020-10-22充满爱意的早上";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-23（又是划水摸鱼的一天）.md": {
	id: "2020/2020-10-23（又是划水摸鱼的一天）.md";
  slug: "2020/2020-10-23又是划水摸鱼的一天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-24(程序员节).md": {
	id: "2020/2020-10-24(程序员节).md";
  slug: "2020/2020-10-24程序员节";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-25(打羽毛球).md": {
	id: "2020/2020-10-25(打羽毛球).md";
  slug: "2020/2020-10-25打羽毛球";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-26(菠菜南瓜粥).md": {
	id: "2020/2020-10-26(菠菜南瓜粥).md";
  slug: "2020/2020-10-26菠菜南瓜粥";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-27(早安打工人).md": {
	id: "2020/2020-10-27(早安打工人).md";
  slug: "2020/2020-10-27早安打工人";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-28(晚餐).md": {
	id: "2020/2020-10-28(晚餐).md";
  slug: "2020/2020-10-28晚餐";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-29（咸味）.md": {
	id: "2020/2020-10-29（咸味）.md";
  slug: "2020/2020-10-29咸味";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-30（摘抄）.md": {
	id: "2020/2020-10-30（摘抄）.md";
  slug: "2020/2020-10-30摘抄";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-10-31（考烤靠）.md": {
	id: "2020/2020-10-31（考烤靠）.md";
  slug: "2020/2020-10-31考烤靠";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-01（跑步）.md": {
	id: "2020/2020-11-01（跑步）.md";
  slug: "2020/2020-11-01跑步";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-02（早起）.md": {
	id: "2020/2020-11-02（早起）.md";
  slug: "2020/2020-11-02早起";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-03（阿范来接我）.md": {
	id: "2020/2020-11-03（阿范来接我）.md";
  slug: "2020/2020-11-03阿范来接我";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-04（自信）.md": {
	id: "2020/2020-11-04（自信）.md";
  slug: "2020/2020-11-04自信";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-06(存款破10w).md": {
	id: "2020/2020-11-06(存款破10w).md";
  slug: "2020/2020-11-06存款破10w";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-07(团建).md": {
	id: "2020/2020-11-07(团建).md";
  slug: "2020/2020-11-07团建";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-08(团建完回家).md": {
	id: "2020/2020-11-08(团建完回家).md";
  slug: "2020/2020-11-08团建完回家";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-09（基金涨势凶猛）.md": {
	id: "2020/2020-11-09（基金涨势凶猛）.md";
  slug: "2020/2020-11-09基金涨势凶猛";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-10(双11).md": {
	id: "2020/2020-11-10(双11).md";
  slug: "2020/2020-11-10双11";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-11（难受）.md": {
	id: "2020/2020-11-11（难受）.md";
  slug: "2020/2020-11-11难受";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-12(脑袋发昏).md": {
	id: "2020/2020-11-12(脑袋发昏).md";
  slug: "2020/2020-11-12脑袋发昏";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-14（患得患失）.md": {
	id: "2020/2020-11-14（患得患失）.md";
  slug: "2020/2020-11-14患得患失";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-15(打球去坪洲逛).md": {
	id: "2020/2020-11-15(打球去坪洲逛).md";
  slug: "2020/2020-11-15打球去坪洲逛";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-16(范做了饭).md": {
	id: "2020/2020-11-16(范做了饭).md";
  slug: "2020/2020-11-16范做了饭";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-17（感冒还没好）.md": {
	id: "2020/2020-11-17（感冒还没好）.md";
  slug: "2020/2020-11-17感冒还没好";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-22（）.md": {
	id: "2020/2020-11-22（）.md";
  slug: "2020/2020-11-22";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-23（早起的虫儿鸟被吃）.md": {
	id: "2020/2020-11-23（早起的虫儿鸟被吃）.md";
  slug: "2020/2020-11-23早起的虫儿鸟被吃";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-27（吃大餐）.md": {
	id: "2020/2020-11-27（吃大餐）.md";
  slug: "2020/2020-11-27吃大餐";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-28(生气吵架).md": {
	id: "2020/2020-11-28(生气吵架).md";
  slug: "2020/2020-11-28生气吵架";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-11-29（入冬的深圳）.md": {
	id: "2020/2020-11-29（入冬的深圳）.md";
  slug: "2020/2020-11-29入冬的深圳";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-12-01（2020的）.md": {
	id: "2020/2020-12-01（2020的）.md";
  slug: "2020/2020-12-012020的";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-12-05（心情烦躁，早起锻炼）.md": {
	id: "2020/2020-12-05（心情烦躁，早起锻炼）.md";
  slug: "2020/2020-12-05心情烦躁早起锻炼";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-12-06(邮政面试).md": {
	id: "2020/2020-12-06(邮政面试).md";
  slug: "2020/2020-12-06邮政面试";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-12-11(找工作包饺子).md": {
	id: "2020/2020-12-11(找工作包饺子).md";
  slug: "2020/2020-12-11找工作包饺子";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-12-12（意难平我）.md": {
	id: "2020/2020-12-12（意难平我）.md";
  slug: "2020/2020-12-12意难平我";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-12-13（自找烦恼）.md": {
	id: "2020/2020-12-13（自找烦恼）.md";
  slug: "2020/2020-12-13自找烦恼";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-12-14(吃酸菜鱼滑冰).md": {
	id: "2020/2020-12-14(吃酸菜鱼滑冰).md";
  slug: "2020/2020-12-14吃酸菜鱼滑冰";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-12-16（真的很不想上班）.md": {
	id: "2020/2020-12-16（真的很不想上班）.md";
  slug: "2020/2020-12-16真的很不想上班";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-12-21(公司聚餐吃乱炖).md": {
	id: "2020/2020-12-21(公司聚餐吃乱炖).md";
  slug: "2020/2020-12-21公司聚餐吃乱炖";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-12-22（落枕第二天）.md": {
	id: "2020/2020-12-22（落枕第二天）.md";
  slug: "2020/2020-12-22落枕第二天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-12-23-25（回家吃饭）.md": {
	id: "2020/2020-12-23-25（回家吃饭）.md";
  slug: "2020/2020-12-23-25回家吃饭";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-12-29（老是生气）.md": {
	id: "2020/2020-12-29（老是生气）.md";
  slug: "2020/2020-12-29老是生气";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2020/2020-12-30（划水）.md": {
	id: "2020/2020-12-30（划水）.md";
  slug: "2020/2020-12-30划水";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-01-01（逛了一天）.md": {
	id: "2021/2021-01-01（逛了一天）.md";
  slug: "2021/2021-01-01逛了一天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-01-02-01-03（玩了两天）.md": {
	id: "2021/2021-01-02-01-03（玩了两天）.md";
  slug: "2021/2021-01-02-01-03玩了两天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-01-07（早起喝粥）.md": {
	id: "2021/2021-01-07（早起喝粥）.md";
  slug: "2021/2021-01-07早起喝粥";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-01-08（周五）.md": {
	id: "2021/2021-01-08（周五）.md";
  slug: "2021/2021-01-08周五";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-01-11（超级冷的一天）.md": {
	id: "2021/2021-01-11（超级冷的一天）.md";
  slug: "2021/2021-01-11超级冷的一天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-01-13（不寻常的昨天）.md": {
	id: "2021/2021-01-13（不寻常的昨天）.md";
  slug: "2021/2021-01-13不寻常的昨天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-01-15（规律的生活）.md": {
	id: "2021/2021-01-15（规律的生活）.md";
  slug: "2021/2021-01-15规律的生活";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-01-16(公司野餐撸猫).md": {
	id: "2021/2021-01-16(公司野餐撸猫).md";
  slug: "2021/2021-01-16公司野餐撸猫";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-01-17（钢铁侠）.md": {
	id: "2021/2021-01-17（钢铁侠）.md";
  slug: "2021/2021-01-17钢铁侠";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-01-23（繁忙周六）.md": {
	id: "2021/2021-01-23（繁忙周六）.md";
  slug: "2021/2021-01-23繁忙周六";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-01-25（进入夏天）.md": {
	id: "2021/2021-01-25（进入夏天）.md";
  slug: "2021/2021-01-25进入夏天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-01-29（下午茶加摔炮）.md": {
	id: "2021/2021-01-29（下午茶加摔炮）.md";
  slug: "2021/2021-01-29下午茶加摔炮";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-01-30 -31（聚餐野游）.md": {
	id: "2021/2021-01-30 -31（聚餐野游）.md";
  slug: "2021/2021-01-30-31聚餐野游";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-01（考公，还书）.md": {
	id: "2021/2021-02-01（考公，还书）.md";
  slug: "2021/2021-02-01考公还书";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-03(吃鱼，玩滑板).md": {
	id: "2021/2021-02-03(吃鱼，玩滑板).md";
  slug: "2021/2021-02-03吃鱼玩滑板";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-04_05(滑板).md": {
	id: "2021/2021-02-04_05(滑板).md";
  slug: "2021/2021-02-04_05滑板";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-06(颓废的一天).md": {
	id: "2021/2021-02-06(颓废的一天).md";
  slug: "2021/2021-02-06颓废的一天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-07(回家前一天总有点感伤).md": {
	id: "2021/2021-02-07(回家前一天总有点感伤).md";
  slug: "2021/2021-02-07回家前一天总有点感伤";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-08(回家回家).md": {
	id: "2021/2021-02-08(回家回家).md";
  slug: "2021/2021-02-08回家回家";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-09(在家的第一天).md": {
	id: "2021/2021-02-09(在家的第一天).md";
  slug: "2021/2021-02-09在家的第一天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-10（阿范来我家）.md": {
	id: "2021/2021-02-10（阿范来我家）.md";
  slug: "2021/2021-02-10阿范来我家";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-11（放炮，去他家）.md": {
	id: "2021/2021-02-11（放炮，去他家）.md";
  slug: "2021/2021-02-11放炮去他家";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-12(大年初一).md": {
	id: "2021/2021-02-12(大年初一).md";
  slug: "2021/2021-02-12大年初一";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-13(大年初二钓鱼).md": {
	id: "2021/2021-02-13(大年初二钓鱼).md";
  slug: "2021/2021-02-13大年初二钓鱼";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-14(今天初三).md": {
	id: "2021/2021-02-14(今天初三).md";
  slug: "2021/2021-02-14今天初三";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-15(初四去华山).md": {
	id: "2021/2021-02-15(初四去华山).md";
  slug: "2021/2021-02-15初四去华山";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-16(初五).md": {
	id: "2021/2021-02-16(初五).md";
  slug: "2021/2021-02-16初五";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-17（初六回深圳）.md": {
	id: "2021/2021-02-17（初六回深圳）.md";
  slug: "2021/2021-02-17初六回深圳";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-18（初七上班有红包）.md": {
	id: "2021/2021-02-18（初七上班有红包）.md";
  slug: "2021/2021-02-18初七上班有红包";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-19（初八）.md": {
	id: "2021/2021-02-19（初八）.md";
  slug: "2021/2021-02-19初八";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-20(周六加班).md": {
	id: "2021/2021-02-20(周六加班).md";
  slug: "2021/2021-02-20周六加班";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-21(休息，我俩一年了，晚上真不高兴).md": {
	id: "2021/2021-02-21(休息，我俩一年了，晚上真不高兴).md";
  slug: "2021/2021-02-21休息我俩一年了晚上真不高兴";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-24(家里下雪了).md": {
	id: "2021/2021-02-24(家里下雪了).md";
  slug: "2021/2021-02-24家里下雪了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-25(买到了很甜的西瓜).md": {
	id: "2021/2021-02-25(买到了很甜的西瓜).md";
  slug: "2021/2021-02-25买到了很甜的西瓜";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-27(周六).md": {
	id: "2021/2021-02-27(周六).md";
  slug: "2021/2021-02-27周六";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-02-28（周末。。。。。。。。。）.md": {
	id: "2021/2021-02-28（周末。。。。。。。。。）.md";
  slug: "2021/2021-02-28周末";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-03-02（坚持了两天跑步）.md": {
	id: "2021/2021-03-02（坚持了两天跑步）.md";
  slug: "2021/2021-03-02坚持了两天跑步";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-03-03（今天周三提前下班）.md": {
	id: "2021/2021-03-03（今天周三提前下班）.md";
  slug: "2021/2021-03-03今天周三提前下班";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-03-05(心情好难过).md": {
	id: "2021/2021-03-05(心情好难过).md";
  slug: "2021/2021-03-05心情好难过";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-03-06(今天去见了一个朋友).md": {
	id: "2021/2021-03-06(今天去见了一个朋友).md";
  slug: "2021/2021-03-06今天去见了一个朋友";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-03-11(周四).md": {
	id: "2021/2021-03-11(周四).md";
  slug: "2021/2021-03-11周四";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-03-13(今天逛了婚博会).md": {
	id: "2021/2021-03-13(今天逛了婚博会).md";
  slug: "2021/2021-03-13今天逛了婚博会";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-03-14(公务员考试).md": {
	id: "2021/2021-03-14(公务员考试).md";
  slug: "2021/2021-03-14公务员考试";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-03-15-16(迪卡侬买了裤子和衬衫).md": {
	id: "2021/2021-03-15-16(迪卡侬买了裤子和衬衫).md";
  slug: "2021/2021-03-15-16迪卡侬买了裤子和衬衫";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-03-17(理发).md": {
	id: "2021/2021-03-17(理发).md";
  slug: "2021/2021-03-17理发";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-03-22(量戒指).md": {
	id: "2021/2021-03-22(量戒指).md";
  slug: "2021/2021-03-22量戒指";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-03-26(怎么融入大家呢).md": {
	id: "2021/2021-03-26(怎么融入大家呢).md";
  slug: "2021/2021-03-26怎么融入大家呢";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-03-28(今天做了鸡爪煲).md": {
	id: "2021/2021-03-28(今天做了鸡爪煲).md";
  slug: "2021/2021-03-28今天做了鸡爪煲";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-03-29-31（今天有在好好锻炼）.md": {
	id: "2021/2021-03-29-31（今天有在好好锻炼）.md";
  slug: "2021/2021-03-29-31今天有在好好锻炼";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-04-01（跑步记录）.md": {
	id: "2021/2021-04-01（跑步记录）.md";
  slug: "2021/2021-04-01跑步记录";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-04-02(今天放假).md": {
	id: "2021/2021-04-02(今天放假).md";
  slug: "2021/2021-04-02今天放假";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-04-03(昨天做的梦太可怕了).md": {
	id: "2021/2021-04-03(昨天做的梦太可怕了).md";
  slug: "2021/2021-04-03昨天做的梦太可怕了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-04-04(吃大渔，省考出成绩).md": {
	id: "2021/2021-04-04(吃大渔，省考出成绩).md";
  slug: "2021/2021-04-04吃大渔省考出成绩";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-04-05（清明的最后一天）.md": {
	id: "2021/2021-04-05（清明的最后一天）.md";
  slug: "2021/2021-04-05清明的最后一天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-04-11(今天在家玩游戏).md": {
	id: "2021/2021-04-11(今天在家玩游戏).md";
  slug: "2021/2021-04-11今天在家玩游戏";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-04-14(放宽心态加油跑步).md": {
	id: "2021/2021-04-14(放宽心态加油跑步).md";
  slug: "2021/2021-04-14放宽心态加油跑步";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-04-16（今天周五）.md": {
	id: "2021/2021-04-16（今天周五）.md";
  slug: "2021/2021-04-16今天周五";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-04-17（下了暗黑破坏神2）.md": {
	id: "2021/2021-04-17（下了暗黑破坏神2）.md";
  slug: "2021/2021-04-17下了暗黑破坏神2";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-04-18（放假前踌躇满志）.md": {
	id: "2021/2021-04-18（放假前踌躇满志）.md";
  slug: "2021/2021-04-18放假前踌躇满志";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-04-21，22(最近压力大，任务重).md": {
	id: "2021/2021-04-21，22(最近压力大，任务重).md";
  slug: "2021/2021-04-2122最近压力大任务重";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-04-23（爷爷生日）.md": {
	id: "2021/2021-04-23（爷爷生日）.md";
  slug: "2021/2021-04-23爷爷生日";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-04-26-27（两天下班都跟晚）.md": {
	id: "2021/2021-04-26-27（两天下班都跟晚）.md";
  slug: "2021/2021-04-26-27两天下班都跟晚";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-05-01－02(顺德之行).md": {
	id: "2021/2021-05-01－02(顺德之行).md";
  slug: "2021/2021-05-0102顺德之行";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-05-03(多梦的一夜).md": {
	id: "2021/2021-05-03(多梦的一夜).md";
  slug: "2021/2021-05-03多梦的一夜";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-05-04（哄好了）.md": {
	id: "2021/2021-05-04（哄好了）.md";
  slug: "2021/2021-05-04哄好了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-05-05（劳动炸东西）.md": {
	id: "2021/2021-05-05（劳动炸东西）.md";
  slug: "2021/2021-05-05劳动炸东西";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-05-07（今天有在努力运动）.md": {
	id: "2021/2021-05-07（今天有在努力运动）.md";
  slug: "2021/2021-05-07今天有在努力运动";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-05-08（今天提前下班，跑步特别有劲）.md": {
	id: "2021/2021-05-08（今天提前下班，跑步特别有劲）.md";
  slug: "2021/2021-05-08今天提前下班跑步特别有劲";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-05-12(操场大变样).md": {
	id: "2021/2021-05-12(操场大变样).md";
  slug: "2021/2021-05-12操场大变样";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-05-14-15（教资面，生气三）.md": {
	id: "2021/2021-05-14-15（教资面，生气三）.md";
  slug: "2021/2021-05-14-15教资面生气三";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-05-16（干点正事）.md": {
	id: "2021/2021-05-16（干点正事）.md";
  slug: "2021/2021-05-16干点正事";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-05-17（今天范休息，买戒指）.md": {
	id: "2021/2021-05-17（今天范休息，买戒指）.md";
  slug: "2021/2021-05-17今天范休息买戒指";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-05-19（今天有在努力运动）.md": {
	id: "2021/2021-05-19（今天有在努力运动）.md";
  slug: "2021/2021-05-19今天有在努力运动";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-05-20（520，-发了一个大红包）.md": {
	id: "2021/2021-05-20（520，-发了一个大红包）.md";
  slug: "2021/2021-05-20520-发了一个大红包";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-05-22(周六取戒指).md": {
	id: "2021/2021-05-22(周六取戒指).md";
  slug: "2021/2021-05-22周六取戒指";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-05-27(接近一周没有记录).md": {
	id: "2021/2021-05-27(接近一周没有记录).md";
  slug: "2021/2021-05-27接近一周没有记录";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-05-30(发现前男，不开心).md": {
	id: "2021/2021-05-30(发现前男，不开心).md";
  slug: "2021/2021-05-30发现前男不开心";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-06-01(错了).md": {
	id: "2021/2021-06-01(错了).md";
  slug: "2021/2021-06-01错了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-06-02(约定三亚拍照).md": {
	id: "2021/2021-06-02(约定三亚拍照).md";
  slug: "2021/2021-06-02约定三亚拍照";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-06-03(耳机到了).md": {
	id: "2021/2021-06-03(耳机到了).md";
  slug: "2021/2021-06-03耳机到了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-06-05(周六放假，百合花开).md": {
	id: "2021/2021-06-05(周六放假，百合花开).md";
  slug: "2021/2021-06-05周六放假百合花开";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-06-06(周末理发).md": {
	id: "2021/2021-06-06(周末理发).md";
  slug: "2021/2021-06-06周末理发";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-06-07（周一整理衣服）.md": {
	id: "2021/2021-06-07（周一整理衣服）.md";
  slug: "2021/2021-06-07周一整理衣服";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-06-08（美甲）.md": {
	id: "2021/2021-06-08（美甲）.md";
  slug: "2021/2021-06-08美甲";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-06-09(牙周炎疼).md": {
	id: "2021/2021-06-09(牙周炎疼).md";
  slug: "2021/2021-06-09牙周炎疼";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-06-11（端午等放假）.md": {
	id: "2021/2021-06-11（端午等放假）.md";
  slug: "2021/2021-06-11端午等放假";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-06-13(端午去三亚).md": {
	id: "2021/2021-06-13(端午去三亚).md";
  slug: "2021/2021-06-13端午去三亚";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-06-14(三亚).md": {
	id: "2021/2021-06-14(三亚).md";
  slug: "2021/2021-06-14三亚";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-06-15(今天拍婚纱照).md": {
	id: "2021/2021-06-15(今天拍婚纱照).md";
  slug: "2021/2021-06-15今天拍婚纱照";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-06-16(选片置气).md": {
	id: "2021/2021-06-16(选片置气).md";
  slug: "2021/2021-06-16选片置气";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-06-17(蜈支洲岛).md": {
	id: "2021/2021-06-17(蜈支洲岛).md";
  slug: "2021/2021-06-17蜈支洲岛";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-06-20(休息的一天).md": {
	id: "2021/2021-06-20(休息的一天).md";
  slug: "2021/2021-06-20休息的一天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-06-21(中午回家下暴雨).md": {
	id: "2021/2021-06-21(中午回家下暴雨).md";
  slug: "2021/2021-06-21中午回家下暴雨";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-06-22（抢到了switch却不纠结买不买）.md": {
	id: "2021/2021-06-22（抢到了switch却不纠结买不买）.md";
  slug: "2021/2021-06-22抢到了switch却不纠结买不买";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-06-25(心).md": {
	id: "2021/2021-06-25(心).md";
  slug: "2021/2021-06-25心";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-07-03(好久没联系的实习同事联系我了).md": {
	id: "2021/2021-07-03(好久没联系的实习同事联系我了).md";
  slug: "2021/2021-07-03好久没联系的实习同事联系我了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-07-05(今天提了离职).md": {
	id: "2021/2021-07-05(今天提了离职).md";
  slug: "2021/2021-07-05今天提了离职";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-07-06（吃瓜吃瓜）.md": {
	id: "2021/2021-07-06（吃瓜吃瓜）.md";
  slug: "2021/2021-07-06吃瓜吃瓜";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-07-11(牙疼脸肿).md": {
	id: "2021/2021-07-11(牙疼脸肿).md";
  slug: "2021/2021-07-11牙疼脸肿";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-07-12(范老弟来接我).md": {
	id: "2021/2021-07-12(范老弟来接我).md";
  slug: "2021/2021-07-12范老弟来接我";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-07-13(牙疼范病).md": {
	id: "2021/2021-07-13(牙疼范病).md";
  slug: "2021/2021-07-13牙疼范病";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-07-13（衣服翻了）.md": {
	id: "2021/2021-07-13（衣服翻了）.md";
  slug: "2021/2021-07-13衣服翻了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-07-17(牙齿好了起来，下午团建吃饭).md": {
	id: "2021/2021-07-17(牙齿好了起来，下午团建吃饭).md";
  slug: "2021/2021-07-17牙齿好了起来下午团建吃饭";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-07-18(周末休息，去吃酸菜鱼).md": {
	id: "2021/2021-07-18(周末休息，去吃酸菜鱼).md";
  slug: "2021/2021-07-18周末休息去吃酸菜鱼";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-07-22(今天已经没任务).md": {
	id: "2021/2021-07-22(今天已经没任务).md";
  slug: "2021/2021-07-22今天已经没任务";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-07-23(今天公司聚餐吃烤羊腿).md": {
	id: "2021/2021-07-23(今天公司聚餐吃烤羊腿).md";
  slug: "2021/2021-07-23今天公司聚餐吃烤羊腿";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-07-24（今天周六买黄金）.md": {
	id: "2021/2021-07-24（今天周六买黄金）.md";
  slug: "2021/2021-07-24今天周六买黄金";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-07-25(周日计划去吃烤羊排).md": {
	id: "2021/2021-07-25(周日计划去吃烤羊排).md";
  slug: "2021/2021-07-25周日计划去吃烤羊排";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-07-26(最后一天上班).md": {
	id: "2021/2021-07-26(最后一天上班).md";
  slug: "2021/2021-07-26最后一天上班";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-07-27（打包回家）.md": {
	id: "2021/2021-07-27（打包回家）.md";
  slug: "2021/2021-07-27打包回家";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-07-28（到家了）.md": {
	id: "2021/2021-07-28（到家了）.md";
  slug: "2021/2021-07-28到家了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-07-29（在家第一天）.md": {
	id: "2021/2021-07-29（在家第一天）.md";
  slug: "2021/2021-07-29在家第一天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-07-30（在家第二天，出门开车）.md": {
	id: "2021/2021-07-30（在家第二天，出门开车）.md";
  slug: "2021/2021-07-30在家第二天出门开车";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-07-31（在家第三天）.md": {
	id: "2021/2021-07-31（在家第三天）.md";
  slug: "2021/2021-07-31在家第三天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-08-01（在家第四天，验视力）.md": {
	id: "2021/2021-08-01（在家第四天，验视力）.md";
  slug: "2021/2021-08-01在家第四天验视力";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-08-02（在家）.md": {
	id: "2021/2021-08-02（在家）.md";
  slug: "2021/2021-08-02在家";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-08-03（大早上被喊去打疫苗）.md": {
	id: "2021/2021-08-03（大早上被喊去打疫苗）.md";
  slug: "2021/2021-08-03大早上被喊去打疫苗";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-08-04（去博爱眼科看眼）.md": {
	id: "2021/2021-08-04（去博爱眼科看眼）.md";
  slug: "2021/2021-08-04去博爱眼科看眼";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-08-05（今天去理发捉蝉）.md": {
	id: "2021/2021-08-05（今天去理发捉蝉）.md";
  slug: "2021/2021-08-05今天去理发捉蝉";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-08-06（今天运动跑10公里）.md": {
	id: "2021/2021-08-06（今天运动跑10公里）.md";
  slug: "2021/2021-08-06今天运动跑10公里";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-08-07（出来聚餐）.md": {
	id: "2021/2021-08-07（出来聚餐）.md";
  slug: "2021/2021-08-07出来聚餐";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-08-08－09（范出成绩了）.md": {
	id: "2021/2021-08-08－09（范出成绩了）.md";
  slug: "2021/2021-08-0809范出成绩了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-08-11-13（逛河滩，治眼）.md": {
	id: "2021/2021-08-11-13（逛河滩，治眼）.md";
  slug: "2021/2021-08-11-13逛河滩治眼";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-08-14（今天七夕）.md": {
	id: "2021/2021-08-14（今天七夕）.md";
  slug: "2021/2021-08-14今天七夕";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-08-17（夏天里最遗憾的事）.md": {
	id: "2021/2021-08-17（夏天里最遗憾的事）.md";
  slug: "2021/2021-08-17夏天里最遗憾的事";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-08-18（复查视力）.md": {
	id: "2021/2021-08-18（复查视力）.md";
  slug: "2021/2021-08-18复查视力";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-08-23（出来玩）.md": {
	id: "2021/2021-08-23（出来玩）.md";
  slug: "2021/2021-08-23出来玩";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-08-24-25（在家的日子太舒服）.md": {
	id: "2021/2021-08-24-25（在家的日子太舒服）.md";
  slug: "2021/2021-08-24-25在家的日子太舒服";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-08-26_28（出来溜达）.md": {
	id: "2021/2021-08-26_28（出来溜达）.md";
  slug: "2021/2021-08-26_28出来溜达";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-08-30（真的很委屈）.md": {
	id: "2021/2021-08-30（真的很委屈）.md";
  slug: "2021/2021-08-30真的很委屈";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-09-01(九月第一天).md": {
	id: "2021/2021-09-01(九月第一天).md";
  slug: "2021/2021-09-01九月第一天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-09-02(河滩逛一逛).md": {
	id: "2021/2021-09-02(河滩逛一逛).md";
  slug: "2021/2021-09-02河滩逛一逛";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-09-04-05(订婚).md": {
	id: "2021/2021-09-04-05(订婚).md";
  slug: "2021/2021-09-04-05订婚";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-09-08(从没把我的话放在心上).md": {
	id: "2021/2021-09-08(从没把我的话放在心上).md";
  slug: "2021/2021-09-08从没把我的话放在心上";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-09-11(就这8月15的月亮能圆).md": {
	id: "2021/2021-09-11(就这8月15的月亮能圆).md";
  slug: "2021/2021-09-11就这8月15的月亮能圆";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-09-12(昨晚做了一夜梦).md": {
	id: "2021/2021-09-12(昨晚做了一夜梦).md";
  slug: "2021/2021-09-12昨晚做了一夜梦";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-09-13-14(周一去看车).md": {
	id: "2021/2021-09-13-14(周一去看车).md";
  slug: "2021/2021-09-13-14周一去看车";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-09-19（今天和姑父去看车）.md": {
	id: "2021/2021-09-19（今天和姑父去看车）.md";
  slug: "2021/2021-09-19今天和姑父去看车";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-09-21（中秋订婚）.md": {
	id: "2021/2021-09-21（中秋订婚）.md";
  slug: "2021/2021-09-21中秋订婚";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-09-23（总感觉今天要写点什么）.md": {
	id: "2021/2021-09-23（总感觉今天要写点什么）.md";
  slug: "2021/2021-09-23总感觉今天要写点什么";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-09-26－27（今天去泉舜上班）.md": {
	id: "2021/2021-09-26－27（今天去泉舜上班）.md";
  slug: "2021/2021-09-2627今天去泉舜上班";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-09-29（又去面试了）.md": {
	id: "2021/2021-09-29（又去面试了）.md";
  slug: "2021/2021-09-29又去面试了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-10-01-02.md": {
	id: "2021/2021-10-01-02.md";
  slug: "2021/2021-10-01-02";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-10-03（憋屈加疏导）.md": {
	id: "2021/2021-10-03（憋屈加疏导）.md";
  slug: "2021/2021-10-03憋屈加疏导";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-10-04（泉舜买包）.md": {
	id: "2021/2021-10-04（泉舜买包）.md";
  slug: "2021/2021-10-04泉舜买包";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-10-05(订车).md": {
	id: "2021/2021-10-05(订车).md";
  slug: "2021/2021-10-05订车";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-10-10(看家具).md": {
	id: "2021/2021-10-10(看家具).md";
  slug: "2021/2021-10-10看家具";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-10-11-13（和父母去看家具13号上班）.md": {
	id: "2021/2021-10-11-13（和父母去看家具13号上班）.md";
  slug: "2021/2021-10-11-13和父母去看家具13号上班";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-10-14（看结婚日）.md": {
	id: "2021/2021-10-14（看结婚日）.md";
  slug: "2021/2021-10-14看结婚日";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-10-15（遇事不要慌，碰车）.md": {
	id: "2021/2021-10-15（遇事不要慌，碰车）.md";
  slug: "2021/2021-10-15遇事不要慌碰车";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-10-16－17（去八中考试，去看车展）.md": {
	id: "2021/2021-10-16－17（去八中考试，去看车展）.md";
  slug: "2021/2021-10-1617去八中考试去看车展";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-10-19（请假去事务科）---草稿.md": {
	id: "2021/2021-10-19（请假去事务科）---草稿.md";
  slug: "2021/2021-10-19请假去事务科---草稿";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-10-21-22(周四去见，周五闲聊).md": {
	id: "2021/2021-10-21-22(周四去见，周五闲聊).md";
  slug: "2021/2021-10-21-22周四去见周五闲聊";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-10-23(纠结要不要辞职去干辅警).md": {
	id: "2021/2021-10-23(纠结要不要辞职去干辅警).md";
  slug: "2021/2021-10-23纠结要不要辞职去干辅警";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-10-25--26（上班辞职过生日-交辅警资料）.md": {
	id: "2021/2021-10-25--26（上班辞职过生日-交辅警资料）.md";
  slug: "2021/2021-10-25--26上班辞职过生日-交辅警资料";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-10-28-29（出红薯，静心，锻炼，告别）.md": {
	id: "2021/2021-10-28-29（出红薯，静心，锻炼，告别）.md";
  slug: "2021/2021-10-28-29出红薯静心锻炼告别";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-10-30（辅警体测）.md": {
	id: "2021/2021-10-30（辅警体测）.md";
  slug: "2021/2021-10-30辅警体测";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-10-31（楂红薯）.md": {
	id: "2021/2021-10-31（楂红薯）.md";
  slug: "2021/2021-10-31楂红薯";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-11-01（这个月努力跑步）.md": {
	id: "2021/2021-11-01（这个月努力跑步）.md";
  slug: "2021/2021-11-01这个月努力跑步";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-11-04-05（连跑两天）.md": {
	id: "2021/2021-11-04-05（连跑两天）.md";
  slug: "2021/2021-11-04-05连跑两天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-11-06-07（辅警面试挑婚纱）.md": {
	id: "2021/2021-11-06-07（辅警面试挑婚纱）.md";
  slug: "2021/2021-11-06-07辅警面试挑婚纱";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-11-12（做了一个神奇的梦）.md": {
	id: "2021/2021-11-12（做了一个神奇的梦）.md";
  slug: "2021/2021-11-12做了一个神奇的梦";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-11-13_14（拍登记照）.md": {
	id: "2021/2021-11-13_14（拍登记照）.md";
  slug: "2021/2021-11-13_14拍登记照";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-11-19（体检拉家具修车）.md": {
	id: "2021/2021-11-19（体检拉家具修车）.md";
  slug: "2021/2021-11-19体检拉家具修车";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-11-21（修完车找）.md": {
	id: "2021/2021-11-21（修完车找）.md";
  slug: "2021/2021-11-21修完车找";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-11-28（yun检）.md": {
	id: "2021/2021-11-28（yun检）.md";
  slug: "2021/2021-11-28yun检";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-12-01-02（领证）.md": {
	id: "2021/2021-12-01-02（领证）.md";
  slug: "2021/2021-12-01-02领证";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-12-04-05（出来溜达）.md": {
	id: "2021/2021-12-04-05（出来溜达）.md";
  slug: "2021/2021-12-04-05出来溜达";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-12-06（爱过别人，把最好的都给了别人）.md": {
	id: "2021/2021-12-06（爱过别人，把最好的都给了别人）.md";
  slug: "2021/2021-12-06爱过别人把最好的都给了别人";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-12-08（翻出了老胶片）.md": {
	id: "2021/2021-12-08（翻出了老胶片）.md";
  slug: "2021/2021-12-08翻出了老胶片";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-12-09-10（到处跑，通知同学）.md": {
	id: "2021/2021-12-09-10（到处跑，通知同学）.md";
  slug: "2021/2021-12-09-10到处跑通知同学";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-12-11(在家做了一套题，准备面试).md": {
	id: "2021/2021-12-11(在家做了一套题，准备面试).md";
  slug: "2021/2021-12-11在家做了一套题准备面试";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-12-14（司辅面试）.md": {
	id: "2021/2021-12-14（司辅面试）.md";
  slug: "2021/2021-12-14司辅面试";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-12-19_20（产检辅j培训）.md": {
	id: "2021/2021-12-19_20（产检辅j培训）.md";
  slug: "2021/2021-12-19_20产检辅j培训";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-12-24_25_26（试妆同学聚会）.md": {
	id: "2021/2021-12-24_25_26（试妆同学聚会）.md";
  slug: "2021/2021-12-24_25_26试妆同学聚会";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-12-25（试妆同学聚会）.md": {
	id: "2021/2021-12-25（试妆同学聚会）.md";
  slug: "2021/2021-12-25试妆同学聚会";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2021/2021-12-27_28_30（看雪中悍刀行，去看电动车）.md": {
	id: "2021/2021-12-27_28_30（看雪中悍刀行，去看电动车）.md";
  slug: "2021/2021-12-27_28_30看雪中悍刀行去看电动车";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-01-01(结婚).md": {
	id: "2022/2022-01-01(结婚).md";
  slug: "2022/2022-01-01结婚";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-01-02(摘草莓).md": {
	id: "2022/2022-01-02(摘草莓).md";
  slug: "2022/2022-01-02摘草莓";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-01-03(去学校拿卷子改).md": {
	id: "2022/2022-01-03(去学校拿卷子改).md";
  slug: "2022/2022-01-03去学校拿卷子改";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-01-04(回门，下雪，独自闲逛).md": {
	id: "2022/2022-01-04(回门，下雪，独自闲逛).md";
  slug: "2022/2022-01-04回门下雪独自闲逛";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-01-05-06-07(大雁逛，面试，辞).md": {
	id: "2022/2022-01-05-06-07(大雁逛，面试，辞).md";
  slug: "2022/2022-01-05-06-07大雁逛面试辞";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-01-09(给我哥的车保养).md": {
	id: "2022/2022-01-09(给我哥的车保养).md";
  slug: "2022/2022-01-09给我哥的车保养";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-01-12-13(最angry的一天).md": {
	id: "2022/2022-01-12-13(最angry的一天).md";
  slug: "2022/2022-01-12-13最angry的一天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-01-14(村里核酸，范回家).md": {
	id: "2022/2022-01-14(村里核酸，范回家).md";
  slug: "2022/2022-01-14村里核酸范回家";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-01-15-16(去关林，去检查，去河滩).md": {
	id: "2022/2022-01-15-16(去关林，去检查，去河滩).md";
  slug: "2022/2022-01-15-16去关林去检查去河滩";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-01-19-20(mian-和).md": {
	id: "2022/2022-01-19-20(mian-和).md";
  slug: "2022/2022-01-19-20mian-和";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-01-22-23-24(今天放假-聚餐).md": {
	id: "2022/2022-01-22-23-24(今天放假-聚餐).md";
  slug: "2022/2022-01-22-23-24今天放假-聚餐";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-01-25-26(猫请吃饭，提车，串亲戚).md": {
	id: "2022/2022-01-25-26(猫请吃饭，提车，串亲戚).md";
  slug: "2022/2022-01-25-26猫请吃饭提车串亲戚";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-01-27-28(试电能跑多远，去串亲戚).md": {
	id: "2022/2022-01-27-28(试电能跑多远，去串亲戚).md";
  slug: "2022/2022-01-27-28试电能跑多远去串亲戚";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-01-29-30(两年前的今天表白).md": {
	id: "2022/2022-01-29-30(两年前的今天表白).md";
  slug: "2022/2022-01-29-30两年前的今天表白";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-01-31－02-01(大年除夕).md": {
	id: "2022/2022-01-31－02-01(大年除夕).md";
  slug: "2022/2022-01-3102-01大年除夕";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-02-02(初二串亲戚，看花灯).md": {
	id: "2022/2022-02-02(初二串亲戚，看花灯).md";
  slug: "2022/2022-02-02初二串亲戚看花灯";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-02-03(初三，在家学习，出去吃饭).md": {
	id: "2022/2022-02-03(初三，在家学习，出去吃饭).md";
  slug: "2022/2022-02-03初三在家学习出去吃饭";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-02-04-05(去姑姑家，抓娃娃，-放风筝).md": {
	id: "2022/2022-02-04-05(去姑姑家，抓娃娃，-放风筝).md";
  slug: "2022/2022-02-04-05去姑姑家抓娃娃-放风筝";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-02-06-07-08(初六在家看电影).md": {
	id: "2022/2022-02-06-07-08(初六在家看电影).md";
  slug: "2022/2022-02-06-07-08初六在家看电影";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-02-09(放假最后一天).md": {
	id: "2022/2022-02-09(放假最后一天).md";
  slug: "2022/2022-02-09放假最后一天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-02-11(开工利是).md": {
	id: "2022/2022-02-11(开工利是).md";
  slug: "2022/2022-02-11开工利是";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-02-12-13(有了个表，去宝龙).md": {
	id: "2022/2022-02-12-13(有了个表，去宝龙).md";
  slug: "2022/2022-02-12-13有了个表去宝龙";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-02-14(果果生日，送范回家).md": {
	id: "2022/2022-02-14(果果生日，送范回家).md";
  slug: "2022/2022-02-14果果生日送范回家";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-02-15-16(泉舜nian，被贴单).md": {
	id: "2022/2022-02-15-16(泉舜nian，被贴单).md";
  slug: "2022/2022-02-15-16泉舜nian被贴单";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-02-17(今天下雪).md": {
	id: "2022/2022-02-17(今天下雪).md";
  slug: "2022/2022-02-17今天下雪";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-02-18-19(范回家).md": {
	id: "2022/2022-02-18-19(范回家).md";
  slug: "2022/2022-02-18-19范回家";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-02-20（去少林寺）.md": {
	id: "2022/2022-02-20（去少林寺）.md";
  slug: "2022/2022-02-20去少林寺";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-02-23-24(带范回家，没找到不高兴).md": {
	id: "2022/2022-02-23-24(带范回家，没找到不高兴).md";
  slug: "2022/2022-02-23-24带范回家没找到不高兴";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-02-26-27（今天周日去，买花）.md": {
	id: "2022/2022-02-26-27（今天周日去，买花）.md";
  slug: "2022/2022-02-26-27今天周日去买花";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-03-04（昨天半夜做梦被范叫醒了）.md": {
	id: "2022/2022-03-04（昨天半夜做梦被范叫醒了）.md";
  slug: "2022/2022-03-04昨天半夜做梦被范叫醒了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-03-05-06（照思维，买电视，看海豚）.md": {
	id: "2022/2022-03-05-06（照思维，买电视，看海豚）.md";
  slug: "2022/2022-03-05-06照思维买电视看海豚";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-03-10（买到了xbox-s）.md": {
	id: "2022/2022-03-10（买到了xbox-s）.md";
  slug: "2022/2022-03-10买到了xbox-s";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-03-13-14(去贴膜，奶奶回来了).md": {
	id: "2022/2022-03-13-14(去贴膜，奶奶回来了).md";
  slug: "2022/2022-03-13-14去贴膜奶奶回来了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-03-19-20(去植物园，把橙子滑板蹲坏了).md": {
	id: "2022/2022-03-19-20(去植物园，把橙子滑板蹲坏了).md";
  slug: "2022/2022-03-19-20去植物园把橙子滑板蹲坏了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-03-24_26瞎折腾，要回家.md": {
	id: "2022/2022-03-24_26瞎折腾，要回家.md";
  slug: "2022/2022-03-24_26瞎折腾要回家";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-03-28(今天理发).md": {
	id: "2022/2022-03-28(今天理发).md";
  slug: "2022/2022-03-28今天理发";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-03-29_30（去哄他）.md": {
	id: "2022/2022-03-29_30（去哄他）.md";
  slug: "2022/2022-03-29_30去哄他";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-04-01-02（接他回来，公司春游）.md": {
	id: "2022/2022-04-01-02（接他回来，公司春游）.md";
  slug: "2022/2022-04-01-02接他回来公司春游";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-04-03-04-05（清明露营）.md": {
	id: "2022/2022-04-03-04-05（清明露营）.md";
  slug: "2022/2022-04-03-04-05清明露营";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-04-07（河滩跑步）.md": {
	id: "2022/2022-04-07（河滩跑步）.md";
  slug: "2022/2022-04-07河滩跑步";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-04-08(周五爷爷生日).md": {
	id: "2022/2022-04-08(周五爷爷生日).md";
  slug: "2022/2022-04-08周五爷爷生日";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-04-10(休息，范提前过生日).md": {
	id: "2022/2022-04-10(休息，范提前过生日).md";
  slug: "2022/2022-04-10休息范提前过生日";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-04-16(大张买东西撞车).md": {
	id: "2022/2022-04-16(大张买东西撞车).md";
  slug: "2022/2022-04-16大张买东西撞车";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-04-21（吵架第五天）.md": {
	id: "2022/2022-04-21（吵架第五天）.md";
  slug: "2022/2022-04-21吵架第五天";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-04-23(今天吃烧烤).md": {
	id: "2022/2022-04-23(今天吃烧烤).md";
  slug: "2022/2022-04-23今天吃烧烤";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-05-01(五一又吵架).md": {
	id: "2022/2022-05-01(五一又吵架).md";
  slug: "2022/2022-05-01五一又吵架";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-05-09(昨夜梦).md": {
	id: "2022/2022-05-09(昨夜梦).md";
  slug: "2022/2022-05-09昨夜梦";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-05-15(昨天吵架今天又是).md": {
	id: "2022/2022-05-15(昨天吵架今天又是).md";
  slug: "2022/2022-05-15昨天吵架今天又是";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-05-20(河滩逛，晚上气).md": {
	id: "2022/2022-05-20(河滩逛，晚上气).md";
  slug: "2022/2022-05-20河滩逛晚上气";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-05-22(昨日生气，周日去宏进市场).md": {
	id: "2022/2022-05-22(昨日生气，周日去宏进市场).md";
  slug: "2022/2022-05-22昨日生气周日去宏进市场";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-05-24(今天买衣服，又生气).md": {
	id: "2022/2022-05-24(今天买衣服，又生气).md";
  slug: "2022/2022-05-24今天买衣服又生气";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-05-31(昨天又惹她生气，今天早点回家锻炼).md": {
	id: "2022/2022-05-31(昨天又惹她生气，今天早点回家锻炼).md";
  slug: "2022/2022-05-31昨天又惹她生气今天早点回家锻炼";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-06-04（今天逛）.md": {
	id: "2022/2022-06-04（今天逛）.md";
  slug: "2022/2022-06-04今天逛";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-06-16(昨天我28了).md": {
	id: "2022/2022-06-16(昨天我28了).md";
  slug: "2022/2022-06-16昨天我28了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-06-18(绝不是我想生气的).md": {
	id: "2022/2022-06-18(绝不是我想生气的).md";
  slug: "2022/2022-06-18绝不是我想生气的";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-06-19(送西瓜).md": {
	id: "2022/2022-06-19(送西瓜).md";
  slug: "2022/2022-06-19送西瓜";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-06-24（用我的gopro拍夕阳）.md": {
	id: "2022/2022-06-24（用我的gopro拍夕阳）.md";
  slug: "2022/2022-06-24用我的gopro拍夕阳";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-06-29（宝宝要出生了）.md": {
	id: "2022/2022-06-29（宝宝要出生了）.md";
  slug: "2022/2022-06-29宝宝要出生了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-06-30（宝儿出生了）.md": {
	id: "2022/2022-06-30（宝儿出生了）.md";
  slug: "2022/2022-06-30宝儿出生了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-07-09（今天省考）.md": {
	id: "2022/2022-07-09（今天省考）.md";
  slug: "2022/2022-07-09今天省考";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-07-27(满月宴，吐槽对象家亲戚，cbn).md": {
	id: "2022/2022-07-27(满月宴，吐槽对象家亲戚，cbn).md";
  slug: "2022/2022-07-27满月宴吐槽对象家亲戚cbn";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-08-06(最近燃起了一股希望).md": {
	id: "2022/2022-08-06(最近燃起了一股希望).md";
  slug: "2022/2022-08-06最近燃起了一股希望";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-08-07(看剧 -幸福到万家).md": {
	id: "2022/2022-08-07(看剧 -幸福到万家).md";
  slug: "2022/2022-08-07看剧-幸福到万家";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-08-08(4号一直到今天都没说话，又提到不高兴的事).md": {
	id: "2022/2022-08-08(4号一直到今天都没说话，又提到不高兴的事).md";
  slug: "2022/2022-08-084号一直到今天都没说话又提到不高兴的事";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-08-15(今天同事结婚).md": {
	id: "2022/2022-08-15(今天同事结婚).md";
  slug: "2022/2022-08-15今天同事结婚";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-08-20_23(取快递，大吵一架，离婚).md": {
	id: "2022/2022-08-20_23(取快递，大吵一架，离婚).md";
  slug: "2022/2022-08-20_23取快递大吵一架离婚";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-08-22(细数我俩之间的不愉快).md": {
	id: "2022/2022-08-22(细数我俩之间的不愉快).md";
  slug: "2022/2022-08-22细数我俩之间的不愉快";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-09-06(加班想走了).md": {
	id: "2022/2022-09-06(加班想走了).md";
  slug: "2022/2022-09-06加班想走了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-09-11(范同学结婚).md": {
	id: "2022/2022-09-11(范同学结婚).md";
  slug: "2022/2022-09-11范同学结婚";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-10-01(真是受不了了).md": {
	id: "2022/2022-10-01(真是受不了了).md";
  slug: "2022/2022-10-01真是受不了了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-10-23(还是一样受不了).md": {
	id: "2022/2022-10-23(还是一样受不了).md";
  slug: "2022/2022-10-23还是一样受不了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-11-01(新月份的开始，幸福的开始).md": {
	id: "2022/2022-11-01(新月份的开始，幸福的开始).md";
  slug: "2022/2022-11-01新月份的开始幸福的开始";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-11-21（都结束了，你还有心情-）.md": {
	id: "2022/2022-11-21（都结束了，你还有心情-）.md";
  slug: "2022/2022-11-21都结束了你还有心情-";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-11-30(新手机到了).md": {
	id: "2022/2022-11-30(新手机到了).md";
  slug: "2022/2022-11-30新手机到了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2022/2022-12-01(命中注定).md": {
	id: "2022/2022-12-01(命中注定).md";
  slug: "2022/2022-12-01命中注定";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-01-22（就看看今天多霸道）.md": {
	id: "2023/2023-01-22（就看看今天多霸道）.md";
  slug: "2023/2023-01-22就看看今天多霸道";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-02-04（不尊重我）.md": {
	id: "2023/2023-02-04（不尊重我）.md";
  slug: "2023/2023-02-04不尊重我";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-02-28-（昨天跑了5公里）.md": {
	id: "2023/2023-02-28-（昨天跑了5公里）.md";
  slug: "2023/2023-02-28-昨天跑了5公里";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-03-04(昌河谷)游玩.md": {
	id: "2023/2023-03-04(昌河谷)游玩.md";
  slug: "2023/2023-03-04昌河谷游玩";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-03-10（买房吵架）.md": {
	id: "2023/2023-03-10（买房吵架）.md";
  slug: "2023/2023-03-10买房吵架";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-03-11（孩子发烧了）.md": {
	id: "2023/2023-03-11（孩子发烧了）.md";
  slug: "2023/2023-03-11孩子发烧了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-03-16（范答应我要弟弟了）.md": {
	id: "2023/2023-03-16（范答应我要弟弟了）.md";
  slug: "2023/2023-03-16范答应我要弟弟了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-05-21(孩子生病).md": {
	id: "2023/2023-05-21(孩子生病).md";
  slug: "2023/2023-05-21孩子生病";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-05-25(给孩子买了个玩具).md": {
	id: "2023/2023-05-25(给孩子买了个玩具).md";
  slug: "2023/2023-05-25给孩子买了个玩具";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-05-26 (今天在路上有感好喜欢宝贝啊).md": {
	id: "2023/2023-05-26 (今天在路上有感好喜欢宝贝啊).md";
  slug: "2023/2023-05-26今天在路上有感好喜欢宝贝啊";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-05-27(吵架抛下病房的孩子).md": {
	id: "2023/2023-05-27(吵架抛下病房的孩子).md";
  slug: "2023/2023-05-27吵架抛下病房的孩子";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-05-28(孩子输液跑针了).md": {
	id: "2023/2023-05-28(孩子输液跑针了).md";
  slug: "2023/2023-05-28孩子输液跑针了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-06-03(宝沙发掉下来了).md": {
	id: "2023/2023-06-03(宝沙发掉下来了).md";
  slug: "2023/2023-06-03宝沙发掉下来了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-06-08(中午好吵，没人说，我去说了).md": {
	id: "2023/2023-06-08(中午好吵，没人说，我去说了).md";
  slug: "2023/2023-06-08中午好吵没人说我去说了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-07-27(泉舜逛开车).md": {
	id: "2023/2023-07-27(泉舜逛开车).md";
  slug: "2023/2023-07-27泉舜逛开车";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-07-29(锻炼).md": {
	id: "2023/2023-07-29(锻炼).md";
  slug: "2023/2023-07-29锻炼";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-07-30(无聊逛商场).md": {
	id: "2023/2023-07-30(无聊逛商场).md";
  slug: "2023/2023-07-30无聊逛商场";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-07-31(怎么解决婚后和父母分房问题).md": {
	id: "2023/2023-07-31(怎么解决婚后和父母分房问题).md";
  slug: "2023/2023-07-31怎么解决婚后和父母分房问题";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-08-15(刚回来两天要分家).md": {
	id: "2023/2023-08-15(刚回来两天要分家).md";
  slug: "2023/2023-08-15刚回来两天要分家";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-08-29(宝贝会走路了).md": {
	id: "2023/2023-08-29(宝贝会走路了).md";
  slug: "2023/2023-08-29宝贝会走路了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-09-06(给宝贝买了兔子).md": {
	id: "2023/2023-09-06(给宝贝买了兔子).md";
  slug: "2023/2023-09-06给宝贝买了兔子";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-09-07(早起喝药).md": {
	id: "2023/2023-09-07(早起喝药).md";
  slug: "2023/2023-09-07早起喝药";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-09-28(孩子真是聪明).md": {
	id: "2023/2023-09-28(孩子真是聪明).md";
  slug: "2023/2023-09-28孩子真是聪明";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-09-29(过于自私的一个人).md": {
	id: "2023/2023-09-29(过于自私的一个人).md";
  slug: "2023/2023-09-29过于自私的一个人";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-10-01(弟结婚).md": {
	id: "2023/2023-10-01(弟结婚).md";
  slug: "2023/2023-10-01弟结婚";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-10-05(扬州南京自驾游).md": {
	id: "2023/2023-10-05(扬州南京自驾游).md";
  slug: "2023/2023-10-05扬州南京自驾游";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-10-18(昨天下雨范回来了).md": {
	id: "2023/2023-10-18(昨天下雨范回来了).md";
  slug: "2023/2023-10-18昨天下雨范回来了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-10-19(孩子的眼睛真的大啊).md": {
	id: "2023/2023-10-19(孩子的眼睛真的大啊).md";
  slug: "2023/2023-10-19孩子的眼睛真的大啊";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-10-20(好想走).md": {
	id: "2023/2023-10-20(好想走).md";
  slug: "2023/2023-10-20好想走";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-10-21(和同学吃饭).md": {
	id: "2023/2023-10-21(和同学吃饭).md";
  slug: "2023/2023-10-21和同学吃饭";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-10-22(还是因为房子).md": {
	id: "2023/2023-10-22(还是因为房子).md";
  slug: "2023/2023-10-22还是因为房子";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-10-24(头晕请假，孩子爱滑梯).md": {
	id: "2023/2023-10-24(头晕请假，孩子爱滑梯).md";
  slug: "2023/2023-10-24头晕请假孩子爱滑梯";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-10-26(写了一个记日记的脚本).md": {
	id: "2023/2023-10-26(写了一个记日记的脚本).md";
  slug: "2023/2023-10-26写了一个记日记的脚本";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-10-27(闲的找活干).md": {
	id: "2023/2023-10-27(闲的找活干).md";
  slug: "2023/2023-10-27闲的找活干";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-10-28(睡不着).md": {
	id: "2023/2023-10-28(睡不着).md";
  slug: "2023/2023-10-28睡不着";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-10-29(带着宝子去玩).md": {
	id: "2023/2023-10-29(带着宝子去玩).md";
  slug: "2023/2023-10-29带着宝子去玩";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-10-31(回来又吵架).md": {
	id: "2023/2023-10-31(回来又吵架).md";
  slug: "2023/2023-10-31回来又吵架";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-11-04(骑着新车上班).md": {
	id: "2023/2023-11-04(骑着新车上班).md";
  slug: "2023/2023-11-04骑着新车上班";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
"2023/2023-11-08(教资成绩出来了).md": {
	id: "2023/2023-11-08(教资成绩出来了).md";
  slug: "2023/2023-11-08教资成绩出来了";
  body: string;
  collection: "blog";
  data: InferEntrySchema<"blog">
} & { render(): Render[".md"] };
};

	};

	type DataEntryMap = {
		"img": {
};

	};

	type AnyEntryMap = ContentEntryMap & DataEntryMap;

	type ContentConfig = typeof import("../src/content/config");
}
