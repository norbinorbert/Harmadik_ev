describe("Node Sameple API Endpoints", () => {
  test("GET /codingresources/codingResources", async () => {
    const response = await fetch(
      "https://api.sampleapis.com/codingresources/codingResources"
    );

    expect(response.status).toBe(200);
  });

  test("GET /codingresources/codingResources/:id", async () => {
    const response = await fetch(
      "https://api.sampleapis.com/codingresources/codingResources/2"
    );
    expect(response.status).toBe(200);
  });
});
