// Middleware to handle info subdomain routing
export async function onRequest(context: any) {
  const url = new URL(context.request.url);
  const hostname = url.hostname;

  // If accessing /info on main domains, redirect to info.sagatoy.com
  if (url.pathname === '/info' &&
      (hostname === 'www.sagatoy.com' ||
       hostname === 'sagatoy.com' ||
       hostname.endsWith('.sagatoy.pages.dev'))) {
    return Response.redirect('https://info.sagatoy.com', 301);
  }

  // If accessing info.sagatoy.com at root, redirect to /info to show content
  if ((hostname === 'info.sagatoy.com' || hostname === 'www.info.sagatoy.com') && url.pathname === '/') {
    return Response.redirect(new URL('/info', url), 301);
  }

  // Continue to next middleware or page
  return context.next();
}
