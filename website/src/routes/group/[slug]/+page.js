// A function that returns a group number as slug in sveltekit
// https://kit.svelte.dev/docs#routing-advanced-dynamic-routes
export function load({ params }) {
	return {
		slug: params.slug
	};
}
