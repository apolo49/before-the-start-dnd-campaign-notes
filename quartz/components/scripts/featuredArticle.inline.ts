import { type FullSlug, getFullSlug, pathToRoot, simplifySlug } from "../../util/path"

// Source - https://stackoverflow.com/a/47593316
// Posted by bryc, modified by community. See post 'Timeline' for change history
// Retrieved 2026-05-20, License - CC BY-SA 4.0

function mulberry32(seed: number) {
  return () => {
        seed |= 0;
        seed = seed + 0x6D2B79F5 | 0;
        let imul = Math.imul(seed ^ seed >>> 15, 1 | seed);
        imul = imul + Math.imul(imul ^ imul >>> 7, 61 | imul) ^ imul;
        return ((imul ^ imul >>> 14) >>> 0) / 4294967296;
    };
}

function getRandomIntBasedOnDate(max: number) {
    const date = new Date();
    const seed = date.getTime() % 2**32;
    const getRand = mulberry32((seed)>>>0)
    return Math.floor(getRand() * max);
}

async function navigateToRandomPage() {
    const fullSlug = getFullSlug(window)
    console.log(`Navigating to random page from ${fullSlug}`)
    const data = await fetchData
    const allPosts = Object.keys(data).map((slug) => simplifySlug(slug as FullSlug))
    console.log(`random post: ${allPosts[getRandomIntBasedOnDate(allPosts.length - 1)]}`)
    // window.location.href = `${pathToRoot(fullSlug)}/${allPosts[getRandomIntBasedOnDate(allPosts.length - 1)]}`
}

document.addEventListener("nav", async (e: unknown) => {
  const slug = (e as CustomEventMap["nav"]).detail.url
  const button = document.getElementById("random-page-button")
  button?.removeEventListener("click", navigateToRandomPage)
  button?.addEventListener("click", navigateToRandomPage)
})
