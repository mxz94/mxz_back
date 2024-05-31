export default function (post) {
    return (
        post.slug ? "/" + post.collection +"/" +  post.slug : "/" + post.collection +"/" + (post.data.title
            // remove leading & trailing whitespace
            .trim()
            // output lowercase
            .toLowerCase()
            // replace spaces
            .replace(/\s+/g, '-')
            // remove leading & trailing separtors
            .replace(/^-+|-+$/g, ''))
    )
}