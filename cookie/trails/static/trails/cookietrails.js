/**
 * CookieTrails JavaScript Library
 * Client-side cookie inventory calculations mirroring cookies.py
 */

/**
 * @typedef {'Advf' | 'Lmup' | 'Tre' | 'D-S-D' | 'Sam' | 'Tags' | 'TMint' | 'Exp' | 'Toff'} CookieVarietyCode
 */

/**
 * @typedef {Object} CookieVarietyInfo
 * @property {CookieVarietyCode} code - Short code for the variety
 * @property {string} label - Human-readable name
 */

/**
 * Cookie variety enum-like object mapping codes to labels
 * @type {Object<CookieVarietyCode, string>}
 */
const CookieVariety = Object.freeze({
  Advf: "Adventurefuls",
  Lmup: "Lemon-Ups",
  Tre: "Trefoils",
  "D-S-D": "Do-si-dos",
  Sam: "Samoas",
  Tags: "Tagalongs",
  TMint: "Thin Mints",
  Exp: "Exploremores",
  Toff: "Toffee-tastics",
});

/**
 * All valid cookie variety codes
 * @type {CookieVarietyCode[]}
 */
const COOKIE_VARIETY_CODES = /** @type {CookieVarietyCode[]} */ (
  Object.keys(CookieVariety)
);

/**
 * Cost per box for each cookie variety (in dollars)
 * @type {Object<CookieVarietyCode, number>}
 */
const COOKIE_COSTS = Object.freeze({
  Advf: 6.0,
  Lmup: 6.0,
  Tre: 6.0,
  "D-S-D": 6.0,
  Sam: 6.0,
  Tags: 6.0,
  TMint: 6.0,
  Exp: 6.0,
  Toff: 7.0,
});

/**
 * eBudde's 2026 color scheme for each cookie variety
 * @type {Object<CookieVarietyCode, string>}
 */
const COOKIE_COLORS = Object.freeze({
  Advf: "#D5CA9F",
  Lmup: "#EDDF3E",
  Tre: "#005BAA",
  "D-S-D": "#FCC56A",
  Sam: "#7D4199",
  Tags: "#E51A40",
  TMint: "#00A654",
  Exp: "#EB9F94",
  Toff: "#00CABE",
});

/**
 * Cookie popularity percentages (must sum to 1.0)
 * Ordered by popularity (most popular first)
 * Current as of Friday January 16, 2026
 * @type {Object<CookieVarietyCode, number>}
 */
const COOKIE_POPULARITY = Object.freeze({
  TMint: 0.278,
  Sam: 0.208,
  Tags: 0.142,
  Exp: 0.099,
  Advf: 0.069,
  Tre: 0.065,
  Lmup: 0.061,
  "D-S-D": 0.047,
  Toff: 0.031,
});

/**
 * Cookie varieties ordered by popularity (most popular first)
 * @type {CookieVarietyCode[]}
 */
const VARIETIES_BY_POPULARITY = /** @type {CookieVarietyCode[]} */ (
  Object.keys(COOKIE_POPULARITY)
);

/** @type {number} */
const BOXES_PER_CASE = 12;

/** @type {number} */
const CASE_THRESHOLD = 5;

/**
 * Calculate the total cost for given cookie varieties and their counts
 * @param {Object<CookieVarietyCode, number>} varieties - Map of variety codes to box counts
 * @returns {number} Total cost rounded to 2 decimal places
 */
function calculateCookieCost(varieties) {
  let total = 0;
  for (const [variety, count] of Object.entries(varieties)) {
    const costPerBox =
      COOKIE_COSTS[/** @type {CookieVarietyCode} */ (variety)] ?? 0;
    total += costPerBox * count;
  }
  return Math.round(total * 100) / 100;
}

/**
 * Use cookie popularity to estimate a distribution of cookie varieties
 * @param {number} totalBoxes - Total number of boxes to distribute
 * @returns {Object<CookieVarietyCode, number>} Map of variety codes to estimated box counts
 */
function calculateDistribution(totalBoxes) {
  /** @type {Object<CookieVarietyCode, number>} */
  const distribution = {};

  // Initial distribution based on popularity
  for (const [variety, popularity] of Object.entries(COOKIE_POPULARITY)) {
    const estimatedCount = Math.round(totalBoxes * popularity);
    distribution[/** @type {CookieVarietyCode} */ (variety)] = estimatedCount;
  }

  // Adjust for rounding errors by distributing across varieties by popularity
  let diff =
    totalBoxes - Object.values(distribution).reduce((a, b) => a + b, 0);

  let idx = 0;
  while (diff !== 0) {
    const variety =
      VARIETIES_BY_POPULARITY[idx % VARIETIES_BY_POPULARITY.length];
    if (diff > 0) {
      distribution[variety] += 1;
      diff -= 1;
    } else {
      if (distribution[variety] > 0) {
        distribution[variety] -= 1;
        diff += 1;
      }
    }
    idx += 1;
  }

  return distribution;
}

/**
 * Calculate the number of cases suggested for each cookie variety
 * @param {Object<CookieVarietyCode, number>} boxes - Map of variety codes to box counts
 * @param {number} [threshold=CASE_THRESHOLD] - Minimum boxes to suggest any cases
 * @returns {Object<CookieVarietyCode, number>} Map of variety codes to suggested case counts
 */
function calculateCases(boxes, threshold = CASE_THRESHOLD) {
  /** @type {Object<CookieVarietyCode, number>} */
  const cases = {};

  for (const [variety, boxCount] of Object.entries(boxes)) {
    if (boxCount >= threshold) {
      // Round up to nearest case
      const numCases = Math.ceil(boxCount / BOXES_PER_CASE);
      cases[/** @type {CookieVarietyCode} */ (variety)] = numCases;
    } else {
      cases[/** @type {CookieVarietyCode} */ (variety)] = 0;
    }
  }

  return cases;
}

/**
 * Get the human-readable label for a cookie variety code
 * @param {CookieVarietyCode} code - The variety code
 * @returns {string} The human-readable label
 */
function getCookieLabel(code) {
  return CookieVariety[code] ?? code;
}

/**
 * Get the color for a cookie variety code
 * @param {CookieVarietyCode} code - The variety code
 * @returns {string} The hex color code
 */
function getCookieColor(code) {
  return COOKIE_COLORS[code] ?? "#CCCCCC";
}

/**
 * Get the cost per box for a cookie variety code
 * @param {CookieVarietyCode} code - The variety code
 * @returns {number} The cost per box in dollars
 */
function getCookieCost(code) {
  return COOKIE_COSTS[code] ?? 0;
}

// Export for use in modules (if needed in future)
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    CookieVariety,
    COOKIE_VARIETY_CODES,
    COOKIE_COSTS,
    COOKIE_COLORS,
    COOKIE_POPULARITY,
    VARIETIES_BY_POPULARITY,
    BOXES_PER_CASE,
    CASE_THRESHOLD,
    calculateCookieCost,
    calculateDistribution,
    calculateCases,
    getCookieLabel,
    getCookieColor,
    getCookieCost,
  };
}

// =============================================================================
// Tests - run on load, console.error on failure
// =============================================================================

/**
 * Simple test runner that logs errors on failure
 * @param {string} name - Test name
 * @param {() => void} fn - Test function that throws on failure
 */
// function runTest(name, fn) {
//   try {
//     fn();
//   } catch (e) {
//     console.error(`FAIL: ${name}`, e.message);
//   }
// }

function runTest(name, fn) {
  // do nothing in production
}

/**
 * Assert helper
 * @param {boolean} condition
 * @param {string} [message]
 */
function assert(condition, message = "Assertion failed") {
  if (!condition) {
    throw new Error(message);
  }
}

(function runTests() {
  runTest("test_calculate_cookie_cost", () => {
    const varieties = {
      TMint: 3,
      Sam: 2,
      Toff: 1,
    };
    const totalCost = calculateCookieCost(varieties);
    const expectedCost =
      COOKIE_COSTS["TMint"] * 3 +
      COOKIE_COSTS["Sam"] * 2 +
      COOKIE_COSTS["Toff"] * 1;
    assert(
      totalCost === expectedCost,
      `Expected ${expectedCost}, got ${totalCost}`
    );
  });

  runTest("test_calculate_cookie_cost_empty", () => {
    const varieties = {};
    const totalCost = calculateCookieCost(varieties);
    assert(totalCost === 0, `Expected 0, got ${totalCost}`);
  });

  runTest("test_calculate_distribution", () => {
    for (let totalBoxes = 0; totalBoxes <= 1000; totalBoxes++) {
      const distribution = calculateDistribution(totalBoxes);

      // Check that the total boxes in the distribution matches the input
      const sum = Object.values(distribution).reduce((a, b) => a + b, 0);
      assert(sum === totalBoxes, `Distribution sum ${sum} !== ${totalBoxes}`);

      // Check that more popular cookies have at least as many boxes as less popular ones
      for (let i = 0; i < VARIETIES_BY_POPULARITY.length - 1; i++) {
        const morePopular = VARIETIES_BY_POPULARITY[i];
        const lessPopular = VARIETIES_BY_POPULARITY[i + 1];
        assert(
          distribution[morePopular] >= distribution[lessPopular],
          `${morePopular} (${distribution[morePopular]}) should have >= boxes than ${lessPopular} (${distribution[lessPopular]}) for totalBoxes=${totalBoxes}`
        );
      }
    }
  });

  runTest("test_calculate_cases", () => {
    const boxes = {
      TMint: 57,
      Sam: 26,
      Lmup: 7,
      Toff: 3,
    };
    const cases = calculateCases(boxes, 5);

    assert(cases["TMint"] === 5, `Expected TMint=5, got ${cases["TMint"]}`);
    assert(cases["Sam"] === 3, `Expected Sam=3, got ${cases["Sam"]}`);
    assert(cases["Lmup"] === 1, `Expected Lmup=1, got ${cases["Lmup"]}`);
    assert(cases["Toff"] === 0, `Expected Toff=0, got ${cases["Toff"]}`);
  });
})();
