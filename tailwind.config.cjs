/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	theme: {
		extend: {},
	},
	plugins: [require("@tailwindcss/typography"),require("daisyui")],
	daisyui: {
		themes: ["lofi"],
		darkTheme: "lofi",
		logs: false, // Shows info about daisyUI version and used config in the console when building your CSS
	  }
}
