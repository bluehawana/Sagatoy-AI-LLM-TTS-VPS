// Debug endpoint to check environment bindings and test R2
export async function onRequestGet(context: any) {
  const envKeys = Object.keys(context.env || {});
  const hasContactsBucket = !!context.env?.CONTACTS_BUCKET;

  let r2WriteTest = "not attempted";
  let r2ReadTest = "not attempted";
  let r2ListTest = "not attempted";

  // Try to write, read, and list from R2
  if (context.env?.CONTACTS_BUCKET) {
    try {
      const testKey = `debug/test-${Date.now()}.json`;
      const testValue = JSON.stringify({
        test: true,
        timestamp: new Date().toISOString(),
      });

      // Write test
      await context.env.CONTACTS_BUCKET.put(testKey, testValue, {
        httpMetadata: {
          contentType: "application/json",
        },
      });
      r2WriteTest = "success";

      // Read test
      const readBack = await context.env.CONTACTS_BUCKET.get(testKey);
      r2ReadTest = readBack ? "success" : "failed - no data returned";

      // List test
      const listed = await context.env.CONTACTS_BUCKET.list({ limit: 10 });
      r2ListTest = `success - ${listed.objects.length} objects found`;
    } catch (error: any) {
      r2WriteTest = `error: ${error.message}`;
      r2ReadTest = `error: ${error.message}`;
      r2ListTest = `error: ${error.message}`;
    }
  }

  const debugInfo = {
    timestamp: new Date().toISOString(),
    envKeys: envKeys,
    hasContactsBucket: hasContactsBucket,
    contactsBucketType: context.env?.CONTACTS_BUCKET
      ? typeof context.env.CONTACTS_BUCKET
      : "undefined",
    r2WriteTest: r2WriteTest,
    r2ReadTest: r2ReadTest,
    r2ListTest: r2ListTest,
    cfInfo: {
      colo: context.request.cf?.colo || "unknown",
      country: context.request.cf?.country || "unknown",
    },
  };

  return new Response(JSON.stringify(debugInfo, null, 2), {
    status: 200,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    },
  });
}

export async function onRequestOptions() {
  return new Response(null, {
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    },
  });
}
