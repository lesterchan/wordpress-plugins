<?php
/**
 * Plugin Name: Demo theme shim
 * Description: Calls the template tags a theme would call, so the demo site shows WP-PageNavi and WP-CommentNavi in place. Development environment only.
 *
 * WP-PageNavi and WP-CommentNavi are template tags: a theme calls them in place
 * of the_posts_navigation() and the_comments_navigation(), and if no theme calls
 * them they render nothing at all -- correctly. No bundled theme calls them, so
 * without this file the demo site would look as though both plugins were broken.
 *
 * This is the same shim the two E2E suites use, kept here so what you click
 * through on the demo site is what the tests drive.
 *
 * @package Demo
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Print the post navigation after the main loop.
 *
 * The loop_end hook fires for every WP_Query, including the secondary ones a
 * theme runs for sidebars, so this is confined to the main query on a listing
 * page.
 *
 * @param WP_Query $query The query that has just finished looping.
 * @return void
 */
function demo_pagenavi_after_loop( $query ) {
	if ( ! function_exists( 'wp_pagenavi' ) || ! $query->is_main_query() || is_singular() ) {
		return;
	}

	echo '<div class="demo-nav"><p><em>WP-PageNavi:</em></p>';
	wp_pagenavi();
	echo '</div>';
}
add_action( 'loop_end', 'demo_pagenavi_after_loop' );

/**
 * Print the comment navigation between the comment list and the form.
 *
 * @return void
 */
function demo_commentnavi_after_list() {
	if ( ! function_exists( 'wp_commentnavi' ) ) {
		return;
	}

	echo '<div class="demo-nav"><p><em>WP-CommentNavi:</em></p>';
	wp_commentnavi();
	echo '</div>';
}
add_action( 'comment_form_before', 'demo_commentnavi_after_list' );
