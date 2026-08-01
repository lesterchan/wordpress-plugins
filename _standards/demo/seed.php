<?php
/**
 * Fill the development site with the same fixtures the E2E suites create.
 *
 * Run through bin/seed-demo.sh, which maps this file into the container and
 * calls it with `wp eval-file`. One invocation rather than a hundred `wp post
 * create` calls, because each of those costs a couple of seconds of container
 * start-up and this would otherwise take several minutes.
 *
 * Everything it makes is marked with a meta key, so running it again clears what
 * the last run made and nothing else. Your own posts are left alone.
 *
 * How much to make is the first two arguments, so the amount can be changed
 * without editing this file:
 *
 *     bin/seed-demo.sh              # 200 posts, 100 comments
 *     bin/seed-demo.sh 500 250
 *
 * @package Demo
 */

if ( ! defined( 'WP_CLI' ) ) {
	exit( 1 );
}

const DEMO_FLAG = '_demo_fixture';

/*
 * WP-CLI hands `wp eval-file <file> <arg>...` its arguments as $args.
 *
 * Two hundred posts is twenty pages at the default ten per page, which is the
 * first amount that shows what WP-PageNavi actually does: below about a dozen
 * pages every page number fits in the window, so the ellipses and the jumps to
 * page 10, 20 and 30 never appear and the plugin looks like a plain list.
 */
$demo_posts    = isset( $args[0] ) ? max( 1, (int) $args[0] ) : 200;
$demo_comments = isset( $args[1] ) ? max( 1, (int) $args[1] ) : 100;

/*
 * Five to a page, matching Settings -> Reading rather than the WordPress
 * default of ten. Smaller pages mean more of them, which is the point: the
 * ellipses and the jumps to page 10, 20 and 30 are the part of WP-PageNavi that
 * a short site never shows.
 */
const DEMO_PER_PAGE = 5;

/**
 * Say what is happening, so a run that stalls says where.
 *
 * @param string $message Line to print.
 * @return void
 */
function demo_say( $message ) {
	WP_CLI::log( '    ' . $message );
}

/**
 * Delete everything an earlier run of this script created.
 *
 * @return void
 */
function demo_clear() {
	$existing = get_posts(
		array(
			'post_type'   => 'any',
			'post_status' => 'any',
			'numberposts' => -1,
			'fields'      => 'ids',
			'meta_key'    => DEMO_FLAG, // phpcs:ignore WordPress.DB.SlowDBQuery.slow_db_query_meta_key -- One-off seeding script, not a request.
		)
	);

	foreach ( $existing as $id ) {
		wp_delete_post( $id, true );
	}

	demo_say( sprintf( 'removed %d posts from a previous run', count( $existing ) ) );
}

/**
 * Create a post and mark it as ours.
 *
 * @param array $args Arguments for wp_insert_post().
 * @return int The new post id.
 */
function demo_post( array $args ) {
	$id = wp_insert_post(
		array_merge(
			array(
				'post_status'    => 'publish',
				'post_type'      => 'post',
				'comment_status' => 'open',
			),
			$args
		)
	);

	add_post_meta( $id, DEMO_FLAG, '1' );

	return $id;
}

/**
 * A MySQL datetime a given number of seconds ago, in site local time.
 *
 * @param int $seconds How far back.
 * @return string
 */
function demo_ago( $seconds ) {
	return gmdate( 'Y-m-d H:i:s', current_time( 'timestamp' ) - $seconds ); // phpcs:ignore WordPress.DateTime.CurrentTimeTimestamp -- Matching the local-time column these dates are written into.
}

WP_CLI::log( '==> Clearing anything an earlier run created' );
demo_clear();

/*
 * Pretty permalinks, so /page/2/ and /comment-page-2/ are real URLs to click.
 * The default plain structure makes both of those ordinary pages, which is what
 * makes a pagination plugin look broken when it is not.
 */
WP_CLI::log( '==> Settings' );
global $wp_rewrite;
$wp_rewrite->set_permalink_structure( '/%year%/%monthnum%/%day%/%postname%/' );
$wp_rewrite->flush_rules();
demo_say( 'pretty permalinks on' );

// Comment paging is off in a default install, so a post with a thousand
// comments still has exactly one page of them and WP-CommentNavi renders
// nothing.
update_option( 'page_comments', '1' );
update_option( 'comments_per_page', (string) DEMO_PER_PAGE );
update_option( 'default_comments_page', 'oldest' );
update_option( 'posts_per_page', (string) DEMO_PER_PAGE );
demo_say( sprintf( 'comment paging on, %d posts and comments per page', DEMO_PER_PAGE ) );

WP_CLI::log(
	sprintf(
		'==> WP-PageNavi: %d posts, so the front page is %d pages long',
		$demo_posts,
		(int) ceil( $demo_posts / DEMO_PER_PAGE )
	)
);

// Dated across the whole relative-date ladder, so WP-RelativeDate has something
// to say on every one of them: minutes, hours, Yesterday, days, weeks, and one
// old enough to keep its plain date.
$spread = array(
	5 * MINUTE_IN_SECONDS,
	2 * HOUR_IN_SECONDS,
	26 * HOUR_IN_SECONDS,
	3 * DAY_IN_SECONDS,
	9 * DAY_IN_SECONDS,
	40 * DAY_IN_SECONDS,
);

/*
 * Deferred, and turned back on at the end.
 *
 * Every wp_insert_post() otherwise recounts the terms it touches and clears a
 * pile of caches, which is invisible at twenty-five posts and most of a minute
 * at five hundred.
 */
wp_defer_term_counting( true );
wp_suspend_cache_invalidation( true );

$width = strlen( (string) $demo_posts );

for ( $i = 1; $i <= $demo_posts; $i++ ) {
	// Each post a little older than the last, cycling through the ladder so
	// every relative phrasing is on screen at once rather than three pages of
	// "Today".
	$age = $spread[ ( $i - 1 ) % count( $spread ) ] + $i * 3 * HOUR_IN_SECONDS;

	demo_post(
		array(
			'post_title'   => sprintf( 'Demo post %0' . $width . 'd', $i ),
			'post_content' => sprintf(
				'One of %d posts, so the front page paginates. Scroll down for the WP-PageNavi links.',
				$demo_posts
			),
			'post_date'    => demo_ago( $age ),
		)
	);
}

wp_suspend_cache_invalidation( false );
wp_defer_term_counting( false );

demo_say(
	sprintf(
		'%d posts, the oldest about %d days back',
		$demo_posts,
		(int) round( ( $demo_posts * 3 * HOUR_IN_SECONDS ) / DAY_IN_SECONDS )
	)
);

WP_CLI::log(
	sprintf(
		'==> WP-CommentNavi: one post with %d comments, so %d pages of them',
		$demo_comments,
		(int) ceil( $demo_comments / DEMO_PER_PAGE )
	)
);

$talked_about = demo_post(
	array(
		'post_title'   => 'A much discussed post',
		'post_content' => 'The WP-CommentNavi links are under the list.',
		'post_date'    => demo_ago( 2 * DAY_IN_SECONDS ),
	)
);

// Counted once at the end rather than after every insert.
wp_defer_comment_counting( true );

$comment_width = strlen( (string) $demo_comments );

for ( $i = 1; $i <= $demo_comments; $i++ ) {
	wp_insert_comment(
		array(
			'comment_post_ID'      => $talked_about,
			'comment_content'      => sprintf( 'Comment number %0' . $comment_width . 'd', $i ),
			'comment_author'       => sprintf( 'Commenter %d', $i ),
			'comment_author_email' => sprintf( 'commenter%d@example.com', $i ),
			'comment_approved'     => 1,
			// One a minute, so "oldest first" means what it says. Written all at
			// once they share a timestamp and the order becomes whatever the
			// database felt like.
			'comment_date'         => demo_ago( ( $demo_comments + 1 - $i ) * MINUTE_IN_SECONDS ),
		)
	);
}

wp_defer_comment_counting( false );

demo_say( sprintf( '%d comments, one a minute so the order is stable', $demo_comments ) );

WP_CLI::log( '==> WP-ShowHide, WP-PostRatings and WP-RelativeDate' );

demo_post(
	array(
		'post_title'   => 'Show and hide',
		'post_content' => "A closed block, which is the default:\n\n"
			. '[showhide]The quick brown fox jumps over the lazy dog. '
			. "Nine words up there, which is what the button counts.[/showhide]\n\n"
			. "One that starts open:\n\n"
			. '[showhide hidden="no" type="spoiler" more_text="Read the ending" less_text="Hide the ending"]'
			. "It was the butler.[/showhide]\n\n"
			. "And two on one page, to show their ids do not collide:\n\n"
			. '[showhide type="first"]First body.[/showhide][showhide type="second"]Second body.[/showhide]',
		'post_date'    => demo_ago( 3 * HOUR_IN_SECONDS ),
	)
);

demo_post(
	array(
		'post_title'   => 'Rate this post',
		'post_content' => "The rating control, from WP-PostRatings:\n\n[ratings]\n\n"
			. "And the same rating as a read-only result:\n\n[ratings results=\"true\"]",
		'post_date'    => demo_ago( 20 * MINUTE_IN_SECONDS ),
	)
);

demo_post(
	array(
		'post_title'   => 'Relative dates',
		'post_content' => "This post was published a few minutes ago.\n\n"
			. "Shortcode, with the date: [relativedate]\n\n"
			. "Shortcode, phrase only: [relativedate ago_only=\"true\"]\n\n"
			. 'Time: [relativetime]',
		'post_date'    => demo_ago( 7 * MINUTE_IN_SECONDS ),
	)
);
demo_say( 'three feature posts' );

if ( class_exists( 'WP_PostRatings_Options' ) ) {
	$options = WP_PostRatings_Options::get();

	$options['shape']        = 'star';
	$options['max']          = 5;
	$options['allowtorate']  = 2;
	$options['check_method'] = 0;

	WP_PostRatings_Options::update( $options );

	demo_say( 'WP-PostRatings set to a five star scale anyone may rate, repeatedly' );
}

WP_CLI::success( 'Demo content ready.' );
